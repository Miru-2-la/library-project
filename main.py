import os
import io
import csv
import uuid
from datetime import datetime
from typing import Optional

import qrcode
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import engine, SessionLocal, Base, open_database
from models import Book, Member, Transaction

# create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")
templates = Jinja2Templates(directory="templates")

# --- Pydantic Schemas ---
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str

class MemberCreate(BaseModel):
    name: str
    student_id: str
    email: str

class IssueRequest(BaseModel):
    book_id: int
    member_id: int

# --- helper to make QR codes ---
def make_qr(data: str) -> bytes:
    # I just use qrcode.make, simpler that way
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    db = SessionLocal()
    try:
        # grab all books and count them
        total_books = db.query(Book).count()
        available_books = db.query(Book).filter(Book.is_available == True).count()
        issued_books = total_books - available_books
        total_members = db.query(Member).count()
        all_books = db.query(Book).all()
        all_members = db.query(Member).all()
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "total_books": total_books,
            "available_books": available_books,
            "issued_books": issued_books,
            "total_members": total_members,
            "all_books": all_books,
            "all_members": all_members
        })
    finally:
        db.close()

@app.post("/api/books")
def create_book(book: BookCreate):
    db = SessionLocal()
    try:
        # check if isbn already exists
        if db.query(Book).filter(Book.isbn == book.isbn).first():
            raise HTTPException(status_code=400, detail="ISBN already exists")
        qr_data = str(uuid.uuid4())
        new_book = Book(title=book.title, author=book.author, isbn=book.isbn, qr_code_data=qr_data)
        db.add(new_book)
        db.commit()
        return {"message": "Book added", "book_id": new_book.id}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.post("/api/members")
def register_member(member: MemberCreate):
    db = SessionLocal()
    try:
        if db.query(Member).filter(Member.student_id == member.student_id).first():
            raise HTTPException(status_code=400, detail="Student ID already registered")
        new_member = Member(name=member.name, student_id=member.student_id, email=member.email)
        db.add(new_member)
        db.commit()
        return {"message": "Member added"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.post("/api/issue")
def issue_book(issue_req: IssueRequest):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == issue_req.book_id).first()
        member = db.query(Member).filter(Member.id == issue_req.member_id).first()
        if not book or not member:
            raise HTTPException(status_code=404, detail="Book or member not found")
        if not book.is_available:
            raise HTTPException(status_code=400, detail="Book not available")
        transaction = Transaction(book_id=book.id, member_id=member.id, status="Issued")
        book.is_available = False
        db.add(transaction)
        db.commit()
        return {"message": "Book issued"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.post("/api/return/{transaction_id}")
def return_book(transaction_id: int):
    db = SessionLocal()
    try:
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        if transaction.status == "Returned":
            raise HTTPException(status_code=400, detail="Already returned")
        transaction.return_date = datetime.utcnow()
        transaction.status = "Returned"
        book = db.query(Book).filter(Book.id == transaction.book_id).first()
        book.is_available = True
        db.commit()
        return {"message": "Book returned"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.get("/api/qr/{book_id}")
def get_qr_code(book_id: int):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        # QR encodes the book ID for easy scanning
        qr_bytes = make_qr(str(book.id))
        return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")
    finally:
        db.close()

@app.get("/api/transactions")
def get_transactions(
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    member_name: Optional[str] = None
):
    db = SessionLocal()
    try:
        query = db.query(Transaction)
        if status and status != "All":
            query = query.filter(Transaction.status == status)
        if member_name:
            query = query.join(Member).filter(Member.name.ilike(f"%{member_name}%"))
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Transaction.issue_date >= start_dt)
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Transaction.issue_date <= end_dt)
        transactions = query.order_by(Transaction.issue_date.desc()).limit(100).all()
        result = []
        for t in transactions:
            result.append({
                "id": t.id,
                "book_title": t.book.title,
                "book_isbn": t.book.isbn,
                "member_name": t.member.name,
                "member_student_id": t.member.student_id,
                "issue_date": t.issue_date.strftime("%Y-%m-%d %H:%M"),
                "return_date": t.return_date.strftime("%Y-%m-%d %H:%M") if t.return_date else None,
                "status": t.status
            })
        return result
    finally:
        db.close()

@app.get("/api/export/csv")
def export_csv(
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    member_name: Optional[str] = None
):
    db = SessionLocal()
    try:
        query = db.query(Transaction)
        if status and status != "All":
            query = query.filter(Transaction.status == status)
        if member_name:
            query = query.join(Member).filter(Member.name.ilike(f"%{member_name}%"))
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Transaction.issue_date >= start_dt)
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Transaction.issue_date <= end_dt)
        transactions = query.order_by(Transaction.issue_date.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Book Title", "ISBN", "Member Name", "Student ID", "Issue Date", "Return Date", "Status"])
        for t in transactions:
            writer.writerow([
                t.id, t.book.title, t.book.isbn, t.member.name, t.member.student_id,
                t.issue_date.strftime("%Y-%m-%d %H:%M"),
                t.return_date.strftime("%Y-%m-%d %H:%M") if t.return_date else "",
                t.status
            ])
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=library_report.csv"}
        )
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    isbn = Column(String, unique=True, index=True)
    qr_code_data = Column(String)
    is_available = Column(Boolean, default=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    # notes = Column(String)   # maybe later
    transactions = relationship("Transaction", back_populates="book")

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    student_id = Column(String, unique=True, index=True)
    email = Column(String)
    transactions = relationship("Transaction", back_populates="member")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    issue_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    status = Column(String, default="Issued")
    
    book = relationship("Book", back_populates="transactions")
    member = relationship("Member", back_populates="transactions")

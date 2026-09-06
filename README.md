# Nexus Campus Library System

A full-stack library management system for issuing and returning books using QR code scanning.
Built with FastAPI, SQLAlchemy, and a modern Tailwind CSS dashboard.

## Features
- Real QR scanning – use your device camera to scan book QR codes.
- Advanced filtering – filter transactions by status, date range, and member name.
- Live statistics – doughnut chart and summary cards update in real time.
- CSV export – download filtered transaction reports.
- Responsive UI – glassmorphism design with animations.
- Modular architecture – clean separation of database, models, and routes.

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository:
   git clone <your-repo-url>
   cd library-project

2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   python main.py

4. Open your browser at http://127.0.0.1:8000

## Database Schema

The system uses SQLite by default.
Tables:
- books: id, title, author, isbn, qr_code_data, is_available, added_at
- members: id, name, student_id, email
- transactions: id, book_id, member_id, issue_date, return_date, status

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | / | Dashboard |
| POST | /api/books | Add new book |
| POST | /api/members | Register member |
| POST | /api/issue | Issue a book |
| POST | /api/return/{transaction_id} | Return a book |
| GET  | /api/qr/{book_id} | Get book QR code |
| GET  | /api/transactions | Get filtered transactions |
| GET  | /api/export/csv | Export filtered CSV |
## 🌐 Live Demo
[Click here to view the live app](https://library-project-w08d.onrender.com/)
This project is deployed on Render.  
To deploy your own instance:
1. Push code to GitHub.
2. Create a new Web Service on [Render](https://render.com).
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy and get the live URL.
6. ## 📸 Screenshots
![Dashboard](screenshots/dashboard.png)
![QR Scanner](screenshots/scanner.png)

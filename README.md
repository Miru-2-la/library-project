# 📚 Nexus Campus Library System

A full‑stack library management system for issuing and returning books using **QR code scanning**.  
Built with **FastAPI**, **SQLAlchemy**, and a modern **Tailwind CSS** dashboard.

## ✨ Features
- 📷 **Real QR scanning** – use your device camera to instantly recognize books.
- 🔍 **Advanced filtering** – filter transactions by status, date range, and member name.
- 📊 **Live statistics** – interactive doughnut chart and summary cards update in real time.
- 📥 **CSV export** – download filtered transaction reports.
- 🖥️ **Responsive UI** – glassmorphism design with smooth animations.
- 🧩 **Modular architecture** – clean separation of database, models, and routes.

## 🌐 Live Demo
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-brightgreen)](https://library-project-w08d.onrender.com/)

## 📸 Screenshots

![Dashboard](screenshots/dashboard.png)  
*Admin dashboard with real‑time stats and transaction table.*

![QR Scanner](screenshots/scanner.png)  
*QR scanner modal using camera.*

![Inventory](screenshots/inventory.png)  
*Inventory grid with QR codes.*

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic
- **Frontend:** HTML5, Tailwind CSS, Chart.js, html5-qrcode
- **Database:** SQLite (default), easily switchable to PostgreSQL/MySQL
- **Deployment:** Render

## ⚙️ Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation & Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Miru-2-la/library-project.git
   cd library-project

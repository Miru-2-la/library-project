# 📚 Nexus Campus Library System.

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

*Note: The free instance may take a few seconds to wake up from sleep.*

## 📸 Screenshots

📁 **[View all screenshots](https://github.com/Miru-2-la/library-project/tree/main/SCREENSHOTS)** – Browse the full set of images.

**Dashboard:** Shows the admin dashboard with real-time statistics cards, inventory status chart, and transaction table.  
**QR Scanner:** Demonstrates the camera-based QR scanning modal used for book identification.  
**Inventory Grid:** Displays the collection of books with their QR codes and availability status.

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

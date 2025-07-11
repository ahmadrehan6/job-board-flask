﻿# 📋 Actuarial Job Board

The Walkthrough and Demo Video Link:
https://drive.google.com/file/d/1ZwDbZkPdI6UBrh_sGZxqULveX6IB0PLh/view?usp=sharing

A full-stack actuarial job board that scrapes actuarial job listings from [ActuaryList.com](https://actuarylist.com), stores them in a MySQL database using Flask and SQLAlchemy, and displays them via a modern frontend with tag filtering, pagination, and responsive layout.

---

## 🔧 Tech Stack

- **Backend**: Python, Flask, SQLAlchemy, MySQL
- **Frontend**: HTML, CSS, JavaScript (vanilla or React)
- **Scraper**: Python + Selenium + BeautifulSoup
- **Database**: MySQL

---

## 📁 Project Structure

project/
│
├── app/
│ ├── init.py
│ ├── database.py
│ ├── models.py # SQLAlchemy Job model
│ └── routes.py # Flask API routes
│
├── scraper.py # Selenium scraper for ActuaryList
│
├── static/
│ ├── style.css # Custom styling
│ └── script.js # Interactive frontend logic
│
├── templates/
│ └── index.html # Frontend HTML page
│
├── config.py
├── app.py # Flask app entry point
├── requirements.txt # Python dependencies
└── README.md # This file


---

## ⚙️ Environment Setup

### ✅ Prerequisites

- **Python**: 3.9+
- **Node.js** *(only if using React version)*: v18+ recommended
- **MySQL**: Installed and running
- **Chrome + ChromeDriver**: Installed and on PATH

### 🔽 Clone the Repository


git clone https://github.com/yourusername/actuarial-job-board.git
cd actuarial-job-board

🐍 Python Setup
📦 Create & Activate a Virtual Environment

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

📦 Install Python Dependencies

pip install -r requirements.txt

🛠️ MySQL Database Setup
1. Create the Database

sql
CREATE DATABASE job_board;

2. Apply Migrations (or create tables manually)

from app import db
db.create_all()
exit()

🚀 Running the Application
✅ Flask Backend

python app.py
The server will run at: http://localhost:5000

🕷️ Running the Scraper
📥 Install ChromeDriver
Download from: https://sites.google.com/chromium.org/driver/

Ensure chromedriver is in your PATH or set the path manually in scraper.py:

▶️ Run the Scraper

python scraper.py
This will:

Scrape jobs from https://www.actuarylist.com

Parse title, company, location, tags, job type, and posted date

Insert them into the database (skip duplicates)

📌 Features

✅ Scrapes actuarial jobs from actuarylist.com

✅ Stores jobs in MySQL via SQLAlchemy

✅ RESTful Flask API for job CRUD

✅ Responsive frontend layout

✅ Tag filtering (clickable pills)

✅ Job type badges (Remote, Onsite, Hybrid)

✅ Toggle mobile view

✅ Delete confirmation prompt

✅ No duplicate job insertion

✅ Clean UI with header/footer

🙋‍♂️ Contributing
Pull requests welcome. Open an issue to discuss ideas or report bugs.


# job-board-flask
# job-board-flask

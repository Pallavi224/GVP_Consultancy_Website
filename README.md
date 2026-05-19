
***

# 🌐 GVP Consultancy Website

A full-stack web application designed to manage consultancy inquiries, client requests, and communication efficiently. This project provides a user-friendly interface for clients to submit inquiries and an admin backend to manage them.

***

## 📌 Project Overview

The **GVP Consultancy Website** enables:

* Clients to submit inquiries
* Admin to manage client requests
* Automated email notifications
* Database storage of all submissions

This project is built using Python-based backend technology with a scalable deployment setup on **Render**.

***

## 🛠️ Tech Stack

### Backend

* Python (Flask / FastAPI – based on your implementation)
* SQLAlchemy (ORM)
* PostgreSQL (Database)

### Frontend

* HTML5
* CSS3
* JavaScript

### Deployment

* Render (Web Service + PostgreSQL)
* Gunicorn (Production server)

### Other Tools

* SMTP (Email integration)
* dotenv / environment variables

***

## 📂 Project Structure

```
GVP_Consultancy_Website/
│
├── app.py / main.py         # Main application entry point
├── models.py               # Database models
├── routes.py               # API routes
├── templates/              # HTML templates
├── static/                 # CSS, JS, Images
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── .env                    # Environment variables (not pushed)
```

***

## 🚀 Quick Start (Local Setup)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Pallavi224/GVP_Consultancy_Website.git
cd GVP_Consultancy_Website
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
SECRET_KEY=your_secret_key
```

### 5️⃣ Run Application

```bash
python app.py
```

App will run on:

```
http://127.0.0.1:5000/
```

***

## 🚢 Deploy on Render

### ✅ Step 1: Push Code to GitHub

Make sure your repo contains:

* `requirements.txt`
* Main app file (`app.py` or `main.py`)

***

### ✅ Step 2: Create PostgreSQL Database

1. Go to **Render Dashboard**
2. Click **New → PostgreSQL**
3. Copy **Database URL**

***

### ✅ Step 3: Create Web Service

1. Click **New → Web Service**
2. Connect your GitHub repo
3. Configure:

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
gunicorn app:app
```

*(Replace `app:app` based on your file name)*

***

### ✅ Step 4: Set Environment Variables

Add in Render:

```
DATABASE_URL=your_render_db_url
EMAIL_USER=your_email
EMAIL_PASS=your_app_password
SECRET_KEY=random_secret
PYTHON_VERSION=3.11.9
```

***

### ✅ Step 5: Deploy

Click **Deploy** ✅

***

## 📊 Database Schema

### Table: `inquiries`

| Column Name | Type      | Description     |
| ----------- | --------- | --------------- |
| id          | Integer   | Primary key     |
| name        | String    | Client name     |
| email       | String    | Client email    |
| message     | Text      | Inquiry message |
| created\_at | Timestamp | Submission time |

***

## 📧 Email Notification

When a client submits an inquiry:

**Sample Email Format:**

```
Subject: New Inquiry Received

Name: John Doe
Email: john@example.com
Message: I need consultancy services...
```

***

## 🔐 Environment Variables (Important)

| Variable      | Description                    |
| ------------- | ------------------------------ |
| DATABASE\_URL | PostgreSQL connection string   |
| EMAIL\_USER   | Email address                  |
| EMAIL\_PASS   | App password (not normal pass) |
| SECRET\_KEY   | Security key                   |

***

## 🔧 Troubleshooting

### ❌ Error: requirements.txt not found

✅ Fix:

```bash
pip freeze > requirements.txt
```

***

### ❌ Build fails on Python 3.14

✅ Fix:

```
PYTHON_VERSION=3.11.9
```

***

### ❌ Email not sending

✅ Check:

* App password enabled (Gmail)
* SMTP settings correct

***

## ✅ Future Enhancements

* Admin dashboard
* Authentication (Login system)
* API-based architecture
* Cloud storage integration
* AI-based inquiry classification (you can highlight your OCI GenAI skills here 💡)

***

## 👩‍💻 Author

**Pallavi Kumari**  
Project Engineer | Oracle Apps | SQL | OCI | Python

***

## ⭐ Support

If you found this helpful:

* ⭐ Star the repo
* Share with others

***




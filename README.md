# flask-website
A Flask-based Expense Tracker web application that allows users to register, log in, manage daily expenses, and monitor their spending through an interactive dashboard. Built using Python, Flask, SQLite, Flask-WTF, and SQLAlchemy.
# 💰 Expense Tracker Web Application

## 📌 Project Overview

The Expense Tracker is a web-based application developed using Python and Flask that helps users manage and track their daily expenses.

The application provides user authentication, expense management, and a dashboard to monitor spending, view transaction details, and understand expense distribution across different categories.

## ✨ Features

- **User Registration:** Create a new account.
- **User Login:** Secure authentication using password hashing.
- **User Logout:** Safely end the user session.
- **Dashboard:** View total expenses, transaction count, and category-wise breakdown.
- **Add Expenses:** Record expenses with descriptions, amounts, categories, and dates.
- **View Expenses:** Access individual expense details.
- **Delete Expenses:** Remove unwanted expense records.
- **Database Integration:** Store user and expense information using SQLite.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database management |
| SQLite | Database |
| Flask-WTF | Form handling and validation |
| WTForms | Form validation |
| Werkzeug | Password hashing |
| HTML5 | Webpage structure |
| CSS3 | Styling |
| Jinja2 | Template rendering |

## 📂 Project Structure

```text
Expense-Tracker/
│
├── app.py
├── forms.py
├── expenses.db
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── expense.html
│   └── add_expense.html
│
├── static/
│   └── style.css
│
└── README.md
```

*Note: Adjust the filenames according to your actual project structure.*

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd Expense-Tracker
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-wtf email-validator
```

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 🔐 Security Features

- Password hashing using Werkzeug.
- Session-based user authentication.
- Form validation using Flask-WTF.
- Login protection for expense management features.

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Developing web applications using Flask.
- Implementing user authentication and session management.
- Working with SQLite databases.
- Performing CRUD operations.
- Integrating Flask-SQLAlchemy.
- Creating and validating forms using Flask-WTF.
- Using Jinja2 templates for dynamic web pages.

## 🚀 Future Enhancements

- Expense visualization using charts.
- Monthly and yearly expense reports.
- Expense filtering and search functionality.
- Budget management.
- Exporting expense reports.

## ⚠️ Disclaimer

This project was developed for educational purposes as part of my web development learning journey.

## 👩‍💻 Project Category

**Python | Flask | Web Development | Database Management**

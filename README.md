# 📚 Smart Student Search & Rank System

A simple, beginner-friendly web application to store, search, sort, and rank students by marks — built with Python, Flask, SQLite, HTML, CSS, and basic JavaScript concepts.

This project was built as a learning exercise to understand how a real web application connects a database, backend logic, and frontend pages together — without relying on heavy frameworks like Django. Every line of code is written to be readable and understandable, not just functional.

---

## ✨ Features

- 🔐 **User Login & Registration** — Secure account system with hashed passwords; only logged-in users can manage student data.
- ➕ **Add Student** — Add a new student with Roll Number, Name, and Marks, with input validation (no empty fields, no duplicate roll numbers, marks capped at 100).
- 📋 **View Students** — See every student in a clean table, automatically sorted by Roll Number (ascending).
- 🔍 **Search Student** — Search for students by name (partial matches supported, e.g. searching "an" finds "Anita").
- 🔃 **Sort by Marks** — View all students ordered from highest to lowest marks.
- 🏆 **Rank Students** — See students ranked 1st, 2nd, 3rd... with proper tie-handling (students with equal marks share the same rank), plus medal icons for the top 3.
- ✏️ **Edit Student** — Update any student's Roll Number, Name, or Marks through a pre-filled form.
- 🗑️ **Delete Student** — Remove a student, with a confirmation step to prevent accidental deletion.
- 🎨 **Responsive UI** — Clean, professional design that adapts to desktop, tablet, and mobile screens.
- 🗄️ **SQLite Database** — All data (students and user accounts) is stored permanently in a local `students.db` file.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Database | SQLite |
| Frontend | HTML, CSS |
| Security | Werkzeug password hashing, Flask sessions |

No Django, no JavaScript frameworks, no external databases — kept intentionally simple and beginner-friendly.

---

## 📁 Project Structure

```
smart_student_system/
│
├── app.py                # Main Flask application (all routes/pages logic)
├── database.py            # All database functions (create tables, add/edit/delete/search students & users)
├── students.db             # SQLite database file (auto-created on first run)
│
├── templates/               # All HTML pages
│   ├── index.html            # Home page (menu or login/register prompt)
│   ├── register.html          # Registration page
│   ├── login.html             # Login page
│   ├── add.html               # Add Student form
│   ├── students.html          # View Students table
│   ├── search.html            # Search Student page
│   ├── sorted.html            # Sort by Marks page
│   ├── rank.html               # Rank Students page
│   ├── edit.html                # Edit Student form
│   └── delete.html              # Delete confirmation page
│
├── static/
│   └── style.css              # All styling for every page
│
└── venv/                     # Python virtual environment (not part of the actual project code)
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3 installed on your computer
- VS Code (or any code editor)

### 2. Clone or download the project
Place the project folder (`smart_student_system`) anywhere on your computer, e.g. your Desktop.

### 3. Open a terminal inside the project folder
```bash
cd smart_student_system
```

### 4. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal line once activated.

### 5. Install Flask
```bash
pip install flask
```

### 6. Create the database tables
```bash
python database.py
```

You should see:
```
Database, 'students' table, and 'users' table created successfully!
```

### 7. Run the application
```bash
python app.py
```

### 8. Open in your browser
Go to:
```
http://127.0.0.1:5000
```

---

## 🚀 How to Use

1. **Register** a new account on the home page.
2. **Log in** with your new username and password.
3. Use the menu to **Add**, **View**, **Search**, **Sort**, or **Rank** students.
4. From the **View Students** page, click **Edit** or **Delete** next to any student to manage their record.
5. Click **Logout** on the home page when you're done.

---

## 🔒 Security Notes

- Passwords are never stored as plain text — they are hashed using Werkzeug's `generate_password_hash()` before being saved to the database.
- All student-management pages (Add, View, Search, Sort, Rank, Edit, Delete) are protected behind a login requirement using a custom `@login_required` decorator in `app.py`.
- Deleting a student always requires an explicit confirmation step — simply visiting the delete link never deletes data.

---

## 🧠 Design Decisions

- **Why SQLite instead of manual arrays/hashmaps?** SQLite is a real, lightweight database built into Python, giving us permanent storage, automatic sorting (`ORDER BY`), and fast searching (`LIKE`, unique constraints) without manually implementing data structures — while still being simple enough for a beginner to understand.
- **Why Flask instead of Django?** Flask is a lightweight "microframework" that only gives you the essentials (routing, templates), making it easier to see and understand every part of how the app works — ideal for learning, versus Django's larger built-in feature set which hides more behind the scenes.
- **Why hash passwords?** Storing plain-text passwords is a serious security risk. Hashing ensures that even if the database file were ever exposed, actual passwords could not be read or reused.
- **Why separate GET/POST for Delete?** Using a confirmation page (GET) before the actual deletion (POST) prevents accidental data loss from a single misclick or an automated link crawler.

---

## ✅ Testing Checklist

Use this checklist to verify every feature works correctly:

- [ ] Visiting any student page while logged out redirects to Login
- [ ] Register a new account successfully
- [ ] Registering a duplicate username shows an error
- [ ] Login with correct credentials succeeds
- [ ] Login with wrong password shows an error
- [ ] Add a student with valid data succeeds
- [ ] Add a student with an empty field shows an error
- [ ] Add a student with a duplicate roll number shows an error
- [ ] View Students shows all students sorted by Roll Number (ascending)
- [ ] Search finds partial name matches correctly
- [ ] Search with no matches shows a "not found" message
- [ ] Sort by Marks shows students ordered highest to lowest
- [ ] Rank Students shows correct rank numbers, with ties sharing the same rank
- [ ] Edit Student pre-fills the form and correctly updates data
- [ ] Delete Student shows a confirmation page before deleting
- [ ] Canceling a delete does not remove the student
- [ ] Logout correctly revokes access to protected pages

---

## 📌 Possible Future Improvements (Not in Current Scope)

- Export student list to CSV/PDF
- Pagination for large numbers of students
- "Forgot password" functionality
- Per-user student lists (currently all logged-in users share the same student data)

---

## 👤 Author

Built as a guided, step-by-step learning project to understand Flask, SQLite, and full-stack web development fundamentals.
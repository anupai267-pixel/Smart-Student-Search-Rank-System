from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__)
app.secret_key = "smart-student-system-secret-key"  # used to secure session data

# Make sure both database tables exist as soon as the app starts.
database.create_table()
database.create_users_table()


def login_required(view_function):
    """
    This is a 'decorator'. Placing @login_required above any route function
    means: before running that function, first check if the visitor is logged in.
    If not, redirect them to the login page instead.
    """
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)
    return wrapped_view


@app.route("/")
def home():
    """
    Shows the home page. If the visitor is logged in, show the full feature menu.
    If not, show Login/Register buttons instead.
    """
    is_logged_in = "user_id" in session
    username = session.get("username")
    return render_template("index.html", is_logged_in=is_logged_in, username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET: Show an empty registration form.
    POST: Validate and create a new user account, then redirect to login.
    """
    error_message = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if username == "" or password == "" or confirm_password == "":
            error_message = "All fields are required."
        elif password != confirm_password:
            error_message = "Passwords do not match."
        elif len(password) < 4:
            error_message = "Password must be at least 4 characters long."
        else:
            password_hash = generate_password_hash(password)
            success = database.add_user(username, password_hash)
            if success:
                return redirect(url_for("login"))
            else:
                error_message = f"Username '{username}' is already taken. Please choose another."

    return render_template("register.html", error_message=error_message)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    GET: Show an empty login form.
    POST: Check the entered username/password against the database.
          If correct, store the user's info in the session and redirect to home.
    """
    error_message = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = database.get_user_by_username(username)

        if user is None or not check_password_hash(user["password_hash"], password):
            error_message = "Invalid username or password."
        else:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))

    return render_template("login.html", error_message=error_message)


@app.route("/logout")
def logout():
    """
    Clears the session, logging the user out, then redirects to home.
    """
    session.clear()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    """
    GET: Show an empty form to add a new student.
    POST: Read the submitted form data, save it to the database,
          then redirect to the View Students page.
    """
    error_message = None

    if request.method == "POST":
        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        marks = request.form.get("marks", "").strip()

        if name == "" or roll_no == "" or marks == "":
            error_message = "All fields are required. Please fill in every field."
        elif not roll_no.isdigit():
            error_message = "Roll number must be a positive whole number."
        elif not marks.isdigit():
            error_message = "Marks must be a positive whole number."
        elif int(marks) > 100:
            error_message = "Marks cannot be greater than 100."
        else:
            success = database.add_student(int(roll_no), name, int(marks))
            if success:
                return redirect(url_for("view_students"))
            else:
                error_message = f"Roll number {roll_no} already exists. Please use a different roll number."

    return render_template("add.html", error_message=error_message)


@app.route("/students")
@login_required
def view_students():
    """
    Shows every student currently in the database, in a table.
    """
    students = database.get_all_students()
    return render_template("students.html", students=students)


@app.route("/search")
@login_required
def search_student():
    """
    Shows a search box. If a 'name' query parameter is present in the URL,
    it searches the database and shows matching results.
    """
    query = request.args.get("name", "").strip()
    results = []

    if query != "":
        results = database.search_students_by_name(query)

    return render_template("search.html", query=query, results=results)


@app.route("/sorted")
@login_required
def sorted_students():
    """
    Shows all students sorted by marks, highest first.
    """
    students = database.get_students_sorted_by_marks()
    return render_template("sorted.html", students=students)


@app.route("/rank")
@login_required
def rank_students():
    """
    Shows all students sorted by marks, with a rank number assigned to each.
    """
    students = database.get_students_sorted_by_marks()

    ranked_students = []
    current_rank = 0
    previous_marks = None

    for position, student in enumerate(students, start=1):
        if student["marks"] != previous_marks:
            current_rank = position
            previous_marks = student["marks"]
        ranked_students.append({
            "rank": current_rank,
            "roll_no": student["roll_no"],
            "name": student["name"],
            "marks": student["marks"]
        })

    return render_template("rank.html", ranked_students=ranked_students)


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    """
    GET: Show a form pre-filled with the student's current details.
    POST: Read the updated form data, save changes to the database,
          then redirect to the View Students page.
    """
    student = database.get_student_by_id(student_id)

    if student is None:
        return "Student not found.", 404

    error_message = None

    if request.method == "POST":
        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        marks = request.form.get("marks", "").strip()

        if name == "" or roll_no == "" or marks == "":
            error_message = "All fields are required. Please fill in every field."
        elif not roll_no.isdigit():
            error_message = "Roll number must be a positive whole number."
        elif not marks.isdigit():
            error_message = "Marks must be a positive whole number."
        elif int(marks) > 100:
            error_message = "Marks cannot be greater than 100."
        else:
            success = database.update_student(student_id, int(roll_no), name, int(marks))
            if success:
                return redirect(url_for("view_students"))
            else:
                error_message = f"Roll number {roll_no} already belongs to another student."
                student = {"id": student_id, "roll_no": roll_no, "name": name, "marks": marks}

    return render_template("edit.html", student=student, error_message=error_message)


@app.route("/delete/<int:student_id>")
@login_required
def confirm_delete(student_id):
    """
    Shows a confirmation page before actually deleting a student.
    """
    student = database.get_student_by_id(student_id)

    if student is None:
        return "Student not found.", 404

    return render_template("delete.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    """
    Actually deletes the student from the database, then redirects to View Students.
    """
    database.delete_student(student_id)
    return redirect(url_for("view_students"))


if __name__ == "__main__":
    app.run(debug=True)
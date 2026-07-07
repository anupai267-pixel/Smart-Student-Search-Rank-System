from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# Make sure the database and table exist as soon as the app starts.
database.create_table()


@app.route("/")
def home():
    """
    This function runs when someone visits the home page ("/").
    It shows a simple welcome page with links to every feature.
    """
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
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

        # --- Input validation (Day 20 equivalent: no negative marks, no empty names) ---
        if name == "" or roll_no == "" or marks == "":
            error_message = "All fields are required. Please fill in every field."
        elif not roll_no.isdigit():
            error_message = "Roll number must be a positive whole number."
        elif not marks.isdigit():
            error_message = "Marks must be a positive whole number."
        elif int(marks) > 100:
            error_message = "Marks cannot be greater than 100."
        else:
            # All checks passed, try to save to the database
            success = database.add_student(int(roll_no), name, int(marks))
            if success:
                return redirect(url_for("view_students"))
            else:
                error_message = f"Roll number {roll_no} already exists. Please use a different roll number."

    return render_template("add.html", error_message=error_message)


@app.route("/students")
def view_students():
    """
    Shows every student currently in the database, in a table.
    """
    students = database.get_all_students()
    return render_template("students.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)
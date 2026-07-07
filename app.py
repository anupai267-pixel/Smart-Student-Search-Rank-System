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


@app.route("/search")
def search_student():
    """
    Shows a search box. If a 'name' query parameter is present in the URL
    (e.g. /search?name=an), it searches the database and shows matching results.
    """
    query = request.args.get("name", "").strip()
    results = []

    if query != "":
        results = database.search_students_by_name(query)

    return render_template("search.html", query=query, results=results)


@app.route("/sorted")
def sorted_students():
    """
    Shows all students sorted by marks, highest first.
    """
    students = database.get_students_sorted_by_marks()
    return render_template("sorted.html", students=students)


@app.route("/rank")
def rank_students():
    """
    Shows all students sorted by marks, with a rank number assigned to each.
    Students with equal marks share the same rank (standard ranking rule).
    """
    students = database.get_students_sorted_by_marks()

    ranked_students = []
    current_rank = 0
    previous_marks = None

    for position, student in enumerate(students, start=1):
        if student["marks"] != previous_marks:
            # Marks changed from the previous student, so this is a new rank
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

        # --- Same validation rules as Add Student ---
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
                # Re-fetch so the form still shows what the user just typed, not stale old data
                student = {"id": student_id, "roll_no": roll_no, "name": name, "marks": marks}

    return render_template("edit.html", student=student, error_message=error_message)


@app.route("/delete/<int:student_id>")
def confirm_delete(student_id):
    """
    Shows a confirmation page before actually deleting a student.
    """
    student = database.get_student_by_id(student_id)

    if student is None:
        return "Student not found.", 404

    return render_template("delete.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    """
    Actually deletes the student from the database, then redirects to View Students.
    This only runs when the confirmation form is submitted (POST), never on a simple GET visit.
    """
    database.delete_student(student_id)
    return redirect(url_for("view_students"))


if __name__ == "__main__":
    app.run(debug=True)
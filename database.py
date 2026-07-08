import sqlite3

DATABASE_NAME = "students.db"


def get_connection():
    """
    Creates and returns a connection to our SQLite database file.
    If the file 'students.db' does not exist yet, SQLite creates it automatically.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row  # lets us access columns by name, like row["name"]
    return connection


def create_table():
    """
    Creates the 'students' table if it does not already exist.
    This function is safe to run every time the app starts.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no INTEGER NOT NULL UNIQUE,
            name TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def create_users_table():
    """
    Creates the 'users' table if it does not already exist.
    Stores login accounts: a unique username and a securely hashed password.
    We NEVER store the real password, only its hash.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def add_student(roll_no, name, marks):
    """
    Inserts a new student into the students table.
    Returns True if successful, False if the roll number already exists.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (roll_no, name, marks) VALUES (?, ?, ?)",
            (roll_no, name, marks)
        )
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    connection.close()
    return success


def get_all_students():
    """
    Returns a list of all students in the database, in the order they were added.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students ORDER BY roll_no ASC")
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_student_by_id(student_id):
    """
    Returns a single student matching the given database id, or None if not found.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    connection.close()
    return row


def search_students_by_name(name_query):
    """
    Returns all students whose name contains the given search text (case-insensitive).
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ("%" + name_query + "%",)
    )
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_students_sorted_by_marks():
    """
    Returns all students sorted by marks in descending order (highest first).
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students ORDER BY marks DESC")
    rows = cursor.fetchall()
    connection.close()
    return rows


def update_student(student_id, roll_no, name, marks):
    """
    Updates an existing student's details.
    Returns True if successful, False if the new roll number conflicts with another student.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE students SET roll_no = ?, name = ?, marks = ? WHERE id = ?",
            (roll_no, name, marks, student_id)
        )
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    connection.close()
    return success


def delete_student(student_id):
    """
    Deletes a student from the database by their id.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    connection.commit()
    connection.close()


def add_user(username, password_hash):
    """
    Inserts a new user account. password_hash must already be hashed
    (never pass a plain-text password here).
    Returns True if successful, False if the username is already taken.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    connection.close()
    return success


def get_user_by_username(username):
    """
    Returns a single user matching the given username, or None if not found.
    Used during login to check credentials.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    connection.close()
    return row


if __name__ == "__main__":
    # This block only runs if you execute "python database.py" directly.
    # It's a simple self-test to confirm both tables are created correctly.
    create_table()
    create_users_table()
    print("Database, 'students' table, and 'users' table created successfully!")
    print("Database file location: students.db (in this same folder)")
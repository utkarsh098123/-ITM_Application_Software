import sqlite3

connection = sqlite3.connect(
    "attendance.db",
    check_same_thread=False
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    roll_number TEXT,

    image_path TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER,

    subject_code TEXT,

    date TEXT
)
""")

connection.commit()
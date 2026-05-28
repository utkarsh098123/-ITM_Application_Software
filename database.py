import sqlite3

connection = sqlite3.connect(
    "attendance.db",
    check_same_thread=False
)

# Better row access
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# Performance optimizations
cursor.execute("PRAGMA journal_mode=WAL")
cursor.execute("PRAGMA synchronous=NORMAL")
cursor.execute("PRAGMA temp_store=MEMORY")
cursor.execute("PRAGMA cache_size=-64000")

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    roll_number TEXT UNIQUE NOT NULL,

    image_path TEXT NOT NULL,

    embedding TEXT
)
""")

# Attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER NOT NULL,

    subject_code TEXT NOT NULL,

    date TEXT NOT NULL,

    FOREIGN KEY(student_id)
    REFERENCES students(id)
)
""")

# Fast attendance lookup
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_attendance
ON attendance(student_id, subject_code, date)
""")

# Fast roll lookup
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_roll
ON students(roll_number)
""")

connection.commit()
from fastapi import APIRouter
from database import cursor

router = APIRouter()


@router.get("/attendance-history/{roll_number}")
def attendance_history(roll_number: str):

    cursor.execute(
        """
        SELECT id, name, image_path
        FROM students
        WHERE roll_number = ?
        """,
        (roll_number,)
    )

    student = cursor.fetchone()

    if not student:

        return {
            "message": "Student not found"
        }

    student_id = student[0]
    student_name = student[1]
    image_path = student[2]

    cursor.execute(
        """
        SELECT subject_code, date
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
        """,
        (student_id,)
    )

    records = cursor.fetchall()

    attendance_data = []

    for record in records:

        attendance_data.append({

            "subject_code": record[0],

            "date": record[1]
        })

    return {

        "name": student_name,

        "roll_number": roll_number,

        "image_path": image_path,

        "total_present": len(attendance_data),

        "attendance": attendance_data
    }
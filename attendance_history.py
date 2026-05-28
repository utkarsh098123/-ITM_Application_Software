from fastapi import APIRouter
from database import cursor

router = APIRouter()


@router.get("/attendance-history/{roll_number}")
def attendance_history(roll_number: str):

    cursor.execute("""
        SELECT
            s.name,
            s.roll_number,
            s.image_path,
            a.subject_code,
            a.date
        FROM students s
        LEFT JOIN attendance a
        ON s.id = a.student_id
        WHERE s.roll_number = ?
        ORDER BY a.date DESC
    """, (roll_number,))

    records = cursor.fetchall()

    if not records:

        return {
            "message": "Student not found"
        }

    first = records[0]

    attendance_data = [
        {
            "subject_code": subject_code,
            "date": date
        }
        for _, _, _, subject_code, date in records
        if subject_code
    ]

    return {

        "name": first[0],

        "roll_number": first[1],

        "image_path": first[2],

        "total_present": len(attendance_data),

        "attendance": attendance_data
    }
from fastapi import APIRouter, UploadFile, File, Form
from deepface import DeepFace
from database import cursor, connection
import shutil
import os
from datetime import datetime

router = APIRouter()


@router.post("/mark-attendance")
async def mark_attendance(

    subject_code: str = Form(...),

    image: UploadFile = File(...)
):

    temp_path = "temp.jpg"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    for student in students:

        student_id = student[0]
        name = student[1]
        roll_number = student[2]
        image_path = student[3]

        try:

            result = DeepFace.verify(

                img1_path=temp_path,

                img2_path=image_path,

                model_name="Facenet",

                enforce_detection=True
            )

            print("\n========================")
            print("Student:", name)
            print("Roll:", roll_number)
            print("Verified:", result["verified"])
            print("Distance:", result["distance"])
            print("========================\n")

            if result["verified"]:

                today_date = datetime.now().strftime("%Y-%m-%d")

                cursor.execute(
                    """
                    INSERT INTO attendance
                    (student_id, subject_code, date)
                    VALUES (?, ?, ?)
                    """,
                    (student_id, subject_code, today_date)
                )

                connection.commit()

                if os.path.exists(temp_path):
                    os.remove(temp_path)

                return {
                    "attendance_marked": True,
                    "student_name": name,
                    "roll_number": roll_number,
                    "subject_code": subject_code,
                    "date": today_date
                }

        except Exception as e:

            print(
                f"Face verification failed for {name}: {e}"
            )

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return {
        "attendance_marked": False,
        "message": "Face not recognized"
    }
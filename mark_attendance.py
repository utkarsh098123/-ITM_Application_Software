from fastapi import APIRouter, UploadFile, File, Form
from deepface import DeepFace
from database import cursor, connection
from datetime import datetime
import aiofiles
import os

router = APIRouter()

TEMP_PATH = "temp.jpg"


@router.post("/mark-attendance")
async def mark_attendance(
    subject_code: str = Form(...),
    image: UploadFile = File(...)
):

    try:

        # Save image
        async with aiofiles.open(TEMP_PATH, "wb") as f:
            await f.write(await image.read())

        # Generate uploaded image embedding ONCE
        uploaded_embedding = DeepFace.represent(
            img_path=TEMP_PATH,
            model_name="Facenet",
            enforce_detection=False
        )[0]["embedding"]

        # Fetch only required fields
        cursor.execute("""
            SELECT id, name, roll_number, image_path
            FROM students
        """)

        students = cursor.fetchall()

        today_date = datetime.now().strftime("%Y-%m-%d")

        for student_id, name, roll_number, image_path in students:

            try:

                # Generate student embedding
                student_embedding = DeepFace.represent(
                    img_path=image_path,
                    model_name="Facenet",
                    enforce_detection=False
                )[0]["embedding"]

                # Compare embeddings
                result = DeepFace.verify(
                    img1_path=uploaded_embedding,
                    img2_path=student_embedding,
                    model_name="Facenet",
                    enforce_detection=False
                )

                if result["verified"]:

                    # Check duplicate attendance
                    cursor.execute("""
                        SELECT 1
                        FROM attendance
                        WHERE student_id = ?
                        AND subject_code = ?
                        AND date = ?
                    """, (
                        student_id,
                        subject_code,
                        today_date
                    ))

                    if not cursor.fetchone():

                        cursor.execute("""
                            INSERT INTO attendance
                            (student_id, subject_code, date)
                            VALUES (?, ?, ?)
                        """, (
                            student_id,
                            subject_code,
                            today_date
                        ))

                        connection.commit()

                    return {
                        "attendance_marked": True,
                        "student_name": name,
                        "roll_number": roll_number,
                        "subject_code": subject_code,
                        "date": today_date
                    }

            except Exception:
                continue

        return {
            "attendance_marked": False,
            "message": "Face not recognized"
        }

    finally:

        if os.path.exists(TEMP_PATH):
            os.remove(TEMP_PATH)
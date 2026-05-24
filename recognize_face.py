from fastapi import APIRouter, UploadFile, File
from deepface import DeepFace
from database import cursor
import shutil
import os

router = APIRouter()


@router.post("/recognize-face")
async def recognize_face(
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
                enforce_detection=False
            )

            if result["verified"]:

                os.remove(temp_path)

                return {
                    "matched": True,
                    "student_id": student_id,
                    "name": name,
                    "roll_number": roll_number
                }

        except:
            pass

    os.remove(temp_path)

    return {
        "matched": False
    }
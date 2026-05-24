from fastapi import APIRouter, UploadFile, File, Form
from database import cursor, connection
import shutil

router = APIRouter()


@router.post("/register-student")
async def register_student(

    name: str = Form(...),

    roll_number: str = Form(...),

    image: UploadFile = File(...)
):

    image_path = f"images/students/{roll_number}.jpg"

    with open(image_path, "wb") as buffer:

        shutil.copyfileobj(image.file, buffer)

    cursor.execute(

        "INSERT INTO students (name, roll_number, image_path) VALUES (?, ?, ?)",

        (name, roll_number, image_path)
    )

    connection.commit()

    return {
        "message": "Student Registered Successfully"
    }
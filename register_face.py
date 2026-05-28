from fastapi import APIRouter, UploadFile, File, Form
from deepface import DeepFace
from database import cursor, connection
import aiofiles
import os
import json
import traceback

router = APIRouter()

IMAGE_DIR = "images/students"

os.makedirs(IMAGE_DIR, exist_ok=True)


@router.post("/register-student")
async def register_student(

    name: str = Form(...),

    roll_number: str = Form(...),

    image: UploadFile = File(...)
):

    try:

        image_path = f"{IMAGE_DIR}/{roll_number}.jpg"

        # Prevent duplicate roll numbers
        cursor.execute(
            "SELECT 1 FROM students WHERE roll_number = ?",
            (roll_number,)
        )

        if cursor.fetchone():

            return {
                "message": "Roll number already exists"
            }

        # Async image save
        async with aiofiles.open(image_path, "wb") as buffer:

            await buffer.write(await image.read())

        print("Image Saved")

        # Generate embedding ONCE during registration
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=False
        )[0]["embedding"]

        print("Embedding Generated")

        # Store embedding as JSON string
        embedding_json = json.dumps(embedding)

        cursor.execute(
            """
            INSERT INTO students
            (name, roll_number, image_path, embedding)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                roll_number,
                image_path,
                embedding_json
            )
        )

        connection.commit()

        return {
            "message": "Student Registered Successfully"
        }

    except Exception as e:

        print(traceback.format_exc())

        return {
            "error": str(e)
        }
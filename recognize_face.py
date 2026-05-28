from fastapi import APIRouter, UploadFile, File
from deepface import DeepFace
from database import cursor
import aiofiles
import os
import uuid

router = APIRouter()


@router.post("/recognize-face")
async def recognize_face(
    image: UploadFile = File(...)
):

    temp_path = f"{uuid.uuid4()}.jpg"

    try:

        # Async file save
        async with aiofiles.open(temp_path, "wb") as f:
            await f.write(await image.read())

        # Generate uploaded face embedding ONCE
        uploaded_embedding = DeepFace.represent(
            img_path=temp_path,
            model_name="Facenet",
            enforce_detection=False
        )[0]["embedding"]

        # Fetch only required columns
        cursor.execute("""
            SELECT id, name, roll_number, image_path
            FROM students
        """)

        students = cursor.fetchall()

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

                if result.get("verified"):

                    return {
                        "matched": True,
                        "student_id": student_id,
                        "name": name,
                        "roll_number": roll_number
                    }

            except Exception:
                continue

        return {
            "matched": False
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)
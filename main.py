from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import cursor

from register_face import router as register_router
from recognize_face import router as recognize_router
from mark_attendance import router as attendance_router
from attendance_history import router as history_router


app = FastAPI()


# IMAGE FOLDER ACCESS
app.mount(
    "/images",
    StaticFiles(directory="images"),
    name="images"
)


# ROUTES
app.include_router(register_router)

app.include_router(recognize_router)

app.include_router(attendance_router)

app.include_router(history_router)


# HOME
@app.get("/")
def home():

    return {
        "message": "Backend Running Successfully"
    }


# GET ALL STUDENTS
@app.get("/students")
def get_students():

    cursor.execute(
        "SELECT * FROM students"
    )

    students = cursor.fetchall()

    return {
        "students": students
    }
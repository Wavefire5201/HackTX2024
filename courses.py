import os
import sys
import re
from Iris import Iris
import iris

# Canvas API
import canvasapi
from canvasapi.course import Course
from canvasapi.exceptions import Unauthorized, ResourceDoesNotExist, Forbidden
from canvasapi.file import File
from canvasapi.module import Module, ModuleItem
from pathvalidate import sanitize_filename
from dotenv import load_dotenv

load_dotenv()

CANVAS_API_KEY = os.getenv("CANVAS_API_KEY")
OLLAMA_HOST = os.getenv("OLLAMA_HOST")

iris = Iris(database=True).connect()
cursor = iris.cursor()

user_table = "Users.Profile"
user_df = (
    "(UserID VARCHAR(50) PRIMARY KEY, Name VARCHAR(100), CanvasAPIKey VARCHAR(255))"
)
course_table = "Users.Course"
course_df = """
(
        CourseID IDENTITY PRIMARY KEY,
        UserID VARCHAR(50),
        CourseName VARCHAR(100),
        VectorData VARBINARY(32000),
        Metadata VARCHAR(4000),
        FOREIGN KEY (UserID) REFERENCES Users.Profile(UserID)
    )
"""


def create_schema():
    """Create the database schema."""
    cursor.execute(f"CREATE TABLE {user_table} {user_df}")
    cursor.execute(f"CREATE TABLE {course_table} {course_df}")


def add_user(user_id: str, name: str, api_key: str) -> None:
    """Add a new user to the database."""
    print(
        f"INSERT INTO {user_table} (UserID, Name, CanvasAPIKey) VALUES ('{user_id}', '{name}', '{api_key}')"
    )
    cursor.execute(
        f"INSERT INTO {user_table} (UserID, Name, CanvasAPIKey) VALUES (?, ?, ?)",
        (user_id, name, api_key),
    )


def add_course(
    user_id: str, course_name: str, vector_data: bytes, metadata: str
) -> None:
    """Add a course with vector data for a user."""
    print(
        f"INSERT INTO {course_table} (UserID, CourseName, VectorData, Metadata) VALUES ('{user_id}', '{course_name}', ?, ?)"
    )
    cursor.execute(
        f"INSERT INTO {course_table} (UserID, CourseName, VectorData, Metadata) VALUES (?, ?, ?, ?)",
        (user_id, course_name, vector_data, metadata),
    )


def get_user_courses(user_id: str) -> list[dict]:
    """Retrieve all courses for a user."""
    result = iris.query(
        "SELECT CourseID, CourseName, VectorData, Metadata FROM Users.Course WHERE UserID = ?",
        user_id,
    )

    courses = []
    for row in result:
        courses.append(
            {
                "course_id": row[0],
                "course_name": row[1],
                "vector_data": row[2],
                "metadata": row[3],
            }
        )
    return courses


def update_course_vector(course_id: int, vector_data: bytes, metadata: str) -> None:
    """Update vector data and metadata for a course."""
    print(
        f"UPDATE {course_table} SET VectorData = ?, Metadata = ? WHERE CourseID = {course_id}"
    )
    cursor.execute(
        f"UPDATE {course_table} SET VectorData = ?, Metadata = ? WHERE CourseID = ?",
        (vector_data, metadata, course_id),
    )


def delete_user(user_id: str) -> None:
    """Delete a user and all their associated courses."""
    print(f"DELETE FROM {course_table} WHERE UserID = '{user_id}'")
    cursor.execute(
        f"DELETE FROM {course_table} WHERE UserID = ?; DELETE FROM {user_table} WHERE UserID = ?;",
        (user_id, user_id),
    )


def main():
    try:
        # Initialize connection and schema
        # conn = iris.connect()
        # create_schema()

        # Example: Add a user
        add_user("0", "hello", "canvas_api_key_123")

        # Example: Add courses for the user
        # vector_data1 = b"..."  # Your vector data here
        # metadata1 = '{"course_type": "Math", "difficulty": "Advanced"}'
        # add_course("0", "Calculus 101", vector_data1, metadata1)

        # Example: Retrieve user's courses
        # courses = get_user_courses("0")
        # print(f"Found {len(courses)} courses for user 0")

    except Exception as e:
        print(f"Error: {str(e)}")
    # finally:
    #     conn.close()


if __name__ == "__main__":
    main()

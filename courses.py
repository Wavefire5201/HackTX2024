import os, sys, re
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

# check db for user (add api key and assign id, name, email)
# if user not in db, add user
# if user in db, check courses
#   if course not in db, add course
#   if course in db, check modules
#       if module not in db, add module
#       if module in db, check files
#           if file not in db, add file
#           if file in db, check for updates
#               if update, update file

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


# Create the database schema
def create_schema():
    # Create the main global for users
    cursor.execute(f"CREATE TABLE {user_table} {user_df}")

    # # Create table for courses
    cursor.execute(f"CREATE TABLE {course_table} {course_df}")

    # cursor.execute(f"DROP TABLE {user_table}")

    # # Create table for courses
    # cursor.execute(f"DROP TABLE {course_table}")


# Helper functions for CRUD operations
def add_user(user_id: str, name: str, api_key: str) -> None:
    """Add a new user to the database."""
    print(
        f"INSERT INTO {user_table} (UserID, Name, CanvasAPIKey) VALUES ({user_id}, {name}, {api_key})"
    )
    cursor.execute(
        f"INSERT INTO {user_table}  (UserID, Name, CanvasAPIKey) VALUES ({user_id}, {name}, {api_key})"
    )


def add_course(
    user_id: str, course_name: str, vector_data: bytes, metadata: str
) -> None:
    """Add a course with vector data for a user."""
    cursor.execute(
        """
    INSERT INTO Users.Course (UserID, CourseName, VectorData, Metadata)
    VALUES (?, ?, ?, ?)
    """,
        user_id,
        course_name,
        vector_data,
        metadata,
    )


def get_user_courses(user_id: str) -> list[str, any]:
    """Retrieve all courses for a user."""
    result = iris.query(
        """
    SELECT CourseID, CourseName, VectorData, Metadata
    FROM Users.Course
    WHERE UserID = ?
    """,
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
    cursor.execute(
        """
    UPDATE Users.Course
    SET VectorData = ?, Metadata = ?
    WHERE CourseID = ?
    """,
        vector_data,
        metadata,
        course_id,
    )


def delete_user(user_id: str) -> None:
    """Delete a user and all their associated courses."""
    cursor.execute(
        """
    DELETE FROM Users.Course WHERE UserID = ?;
    DELETE FROM Users.Profile WHERE UserID = ?;
    """,
        user_id,
        user_id,
    )


# Example usage
def main():
    try:
        # Initialize connection and schema
        # conn = iris.connect()
        # create_schema()

        # Example: Add a user
        add_user("0", "'hello'", "'canvas_api_key_123'")

        # # Example: Add courses for the user
        # vector_data1 = b"..."  # Your vector data here
        # metadata1 = '{"course_type": "Math", "difficulty": "Advanced"}'
        # add_course("user123", "Calculus 101", vector_data1, metadata1)

        # # Example: Retrieve user's courses
        # courses = get_user_courses("user123")
        # print(f"Found {len(courses)} courses for user123")

    except Exception as e:
        print(f"Error: {str(e)}")
    # finally:
    #     conn.close()


if __name__ == "__main__":
    main()


# # Initialize a new Canvas object
# canvas = canvasapi.Canvas(API_URL, API_KEY)
# user = canvas.get_current_user()
# courses = user.get_favorite_courses()

# print("- Available courses -")
# i = 1
# for course in courses:
#     course: Course = course

#     print(f"{i:3}| {course.name} ({course.id})")
#     i += 1

# selected_course = input("Select a course: ")
# course = courses[int(selected_course) - 1]

# reindex = (
#     input("Would you like to update the database for this course? (y/N): ").lower()
#     == "y"
# )

# db = chromadb.PersistentClient("./chroma_db")
# try:
#     collection_exists = db.get_collection(course.name.lower().strip().replace(" ", "_"))
# except ValueError:
#     collection_exists = False

# if not collection_exists or reindex:
#     print("Downloading course content...")
#     modules = course.get_modules()

#     def extract_files(text):
#         text_search = re.findall("/files/(\\d+)", text, re.IGNORECASE)
#         groups = set(text_search)
#         return groups

#     output = "./data/"
#     files_downloaded = set()

#     for module in modules:
#         module: Module = module
#         module_items = module.get_module_items()
#         print(f"Module: {module.name}")
#         for item in module_items:
#             item: ModuleItem = item
#             item_type = item.type
#             print(f"{item_type} | {item}")

#             item1 = {key: value for key, value in item.__dict__.items()}
#             # print(item1)

#             path = (
#                 f"{output}/"
#                 f"{sanitize_filename(course.name)}/"
#                 f"{sanitize_filename(module.name)}/"
#             )
#             if not os.path.exists(path):
#                 os.makedirs(path)

#             print(f"{course.name} - " f"{module.name} - " f"{item.title} ({item_type})")

#             if item_type == "File":
#                 file = canvas.get_file(item.content_id)
#                 dest_path = path + sanitize_filename(file.filename)
#                 print(dest_path)
#                 if os.path.isfile(dest_path):
#                     print("Skipping... File already exists...")
#                     pass

#                 files_downloaded.add(item.content_id)
#                 file.download(dest_path)

#             elif item_type == "Page":
#                 page = course.get_page(item.page_url)
#                 with open(
#                     path + sanitize_filename(item.title) + ".html",
#                     "w",
#                     encoding="utf-8",
#                 ) as f:
#                     f.write(page.body or "")
#                 files = extract_files(page.body or "")
#                 for file_id in files:
#                     if file_id in files_downloaded:
#                         continue
#                     try:
#                         file = course.get_file(file_id)
#                         dest_path = path + sanitize_filename(file.filename)

#                         if os.path.isfile(dest_path):
#                             print("Skipping... File already exists...")
#                             pass

#                         files_downloaded.add(file_id)
#                         file.download(dest_path)
#                     except ResourceDoesNotExist or Unauthorized or Forbidden:
#                         pass
#             elif item_type == "Assignment":
#                 assignment = course.get_assignment(item.content_id)
#                 with open(
#                     path + sanitize_filename(item.title) + ".html",
#                     "w",
#                     encoding="utf-8",
#                 ) as f:
#                     f.write(assignment.description or "")
#                 files = extract_files(assignment.description or "")
#                 for file_id in files:
#                     if file_id in files_downloaded:
#                         continue
#                     try:
#                         file = course.get_file(file_id)
#                         dest_path = path + sanitize_filename(file.filename)

#                         if os.path.isfile(dest_path):
#                             print("Skipping... File already exists...")
#                             pass

#                         files_downloaded.add(file_id)
#                         file.download(dest_path)
#                     except ResourceDoesNotExist or Unauthorized or Forbidden:
#                         pass

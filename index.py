from langchain_core.messages import AIMessage
from langchain_iris import IRISVector
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI
import os, dotenv
from Iris import Iris


iris = Iris(database=True).connect()
cursor = iris.cursor()

user_table = "Users.Profile"
user_df = "(Email VARCHAR(100) PRIMARY KEY, Name VARCHAR(100), CanvasKey VARCHAR(255))"
course_table = "Users.Course"
course_df = """
(
        FOREIGN KEY (Email) REFERENCES Users.Profile(Email)
        (CourseID) INT PRIMARY KEY,
        CourseName VARCHAR(100),
        VectorData VECTOR(DOUBLE, 1024),
    )
"""


def create_schema():
    """Create the database schema."""
    cursor.execute(f"CREATE TABLE {user_table} {user_df}")
    cursor.execute(f"CREATE TABLE {course_table} {course_df}")


def delete_schema():
    """Delete the database schema."""
    cursor.execute(f"DROP TABLE {course_table}")
    cursor.execute(f"DROP TABLE {user_table}")


def add_user(user_email: str, name: str, api_key: str) -> None:
    """Add a new user to the database."""
    print(
        f"INSERT INTO {user_table} (UserID, Name, CanvasAPIKey) VALUES ('{user_email}', '{name}', '{api_key}')"
    )
    cursor.execute(
        f"INSERT INTO {user_table} (UserID, Name, CanvasAPIKey) VALUES (?, ?, ?)",
        (user_email, name, api_key),
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


class CourseIndexer:
    def __init__(self):
        dotenv.load_dotenv()
        self.OLLAMA_HOST = os.getenv("OLLAMA_HOST")
        # self.llm = ChatOllama(model="llama3.1:8b", base_url=OLLAMA_HOST)
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text", base_url=self.OLLAMA_HOST
        )
        self.iris = Iris(database=False)

    def index_files(self):
        """Index all files in the database."""
        files = os.listdir("path/to/files")  # Replace with your actual directory path
        for file in files:
            if file.endswith(".txt"):  # Index only text files
                loader = TextLoader(f"path/to/files/{file}", encoding="utf-8")
                documents = loader.load()
                text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20)
                docs = text_splitter.split_documents(documents)

                for doc in docs:
                    vector_data = self.embeddings.embed(doc.content)
                    metadata = {"filename": file, "content": doc.content}
                    add_course(
                        "user_id_placeholder", file, vector_data, metadata
                    )  # Replace user_id_placeholder with actual user ID


def main():
    # try:
    # Initialize connection and schema
    # conn = iris.connect()
    # create_schema()
    # delete_schema()
    # pass

    # Example: Add a user
    add_user("enochzhu@utexas.edu", "'Enoch Zhu'", "'canvas_api_key_123'")

    # except Exception as e:
    #     print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
# loader = TextLoader("../data/state_of_the_union.txt", encoding="utf-8")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20)
# docs = text_splitter.split_documents(documents)

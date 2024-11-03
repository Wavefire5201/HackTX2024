from flask import Flask, request, jsonify  # type: ignore
from flask_cors import CORS  # type: ignore
import iris
import os
import canvasapi
from course_downloader import CourseDownloader  # type: ignore # Import your script

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# Database connection configuration
iris_host = os.getenv("IRIS_HOST")
iris_port = 1972
iris_namespace = os.getenv("IRIS_NAMESPACE")
iris_username = os.getenv("IRIS_USERNAME")
iris_password = os.getenv("IRIS_PASSWORD")


def get_db_connection():
    """Establishes a connection to the InterSystems IRIS database."""
    return iris.connect(
        f"{iris_host} [{iris_namespace}]:{iris_port}", iris_username, iris_password
    )


# Initialize the CourseDownloader instance
downloader = CourseDownloader()


# Endpoint to check if a user exists in the database
@app.route("/check_user", methods=["POST"])
def check_user():
    data = request.json
    canvas_api_key = data.get("apiKey")

    if not canvas_api_key:
        return jsonify({"error": "API key is required"}), 400

    try:
        with get_db_connection() as conn:
            sql = "SELECT UserID FROM Users WHERE CanvasAPIKey = ?"
            stmt = conn.prepare(sql)
            stmt.execute(canvas_api_key)
            result = stmt.fetch()

            if result:
                user_id = result[0]
                return jsonify({"userID": user_id})
            else:
                return jsonify({"userID": None})  # No user found

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to create a new user
@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    canvas_api_key = data.get("apiKey")
    name = data.get("name")  # Optional name parameter

    if not canvas_api_key:
        return jsonify({"error": "API key is required"}), 400

    try:
        with get_db_connection() as conn:
            sql = "INSERT INTO Users (CanvasAPIKey, Name) VALUES (?, ?)"
            stmt = conn.prepare(sql)
            stmt.execute(canvas_api_key, name)
            conn.commit()

            return jsonify({"message": "User created successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to download courses for a given user
@app.route("/send_question", methods=["POST"])
def send_question():
    data = request.json
    question = data.get("question")
    course_id = data.get("course")
    user_id = data.get("userID")

    if not question or not course_id or not user_id:
        return jsonify({"error": "Question, course, and userID are required"}), 400

    # For now, let's assume the question triggers the course download for the user
    try:
        # Use the CourseDownloader to download course content for the given course_id
        downloader.download_course(downloader.canvas.get_course(course_id), course_id)

        # Return a mock answer for testing purposes
        answer = f"Downloaded data for course '{course_id}' for user '{user_id}'"
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)

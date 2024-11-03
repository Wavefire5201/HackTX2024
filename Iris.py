import os, dotenv
import langchain_iris
import iris


class Iris:
    def __init__(self, database: bool):
        dotenv.load_dotenv()
        self.database = database
        self.username = os.getenv("IRIS_USERNAME")
        self.password = os.getenv("IRIS_PASSWORD")
        self.hostname = os.getenv("IRIS_HOST")
        self.port = int(os.getenv("IRIS_PORT"))
        self.namespace = os.getenv("IRIS_NAMESPACE")
        if database:
            self.connection_string = f"{self.hostname}:{self.port}/{self.namespace}"
        else:
            self.connection_string = f"iris://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.namespace}"
        print(self.connection_string)

    def connect(self):
        if self.database:
            return iris.connect(self.connection_string, self.username, self.password)
        return langchain_iris.IrisVector(self.connection_string)

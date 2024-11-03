from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/courses", )

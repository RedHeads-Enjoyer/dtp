from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class GreetRequest(BaseModel):
    name: str


@app.post("/api/greet")
def greet(data: GreetRequest):
    return {"message": f"Привет, {data.name}! Это ответ от FastAPI."}
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/sum/")
def calculate_sum(a: int, b: int):
    return {"result": a + b}


if __name__ == "__main__":
    uvicorn.run('app.homeworks.homework_7_1:app', host="localhost", port=8000, reload=True)

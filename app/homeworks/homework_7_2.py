import requests
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Внешний API URL
EXTERNAL_API_URL = "https://gorest.co.in/public/v2/todos"


# получаем данные из внешнего API
def fetch_todos():
    response = requests.get(url=EXTERNAL_API_URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


# функция для обработки данных
def data_values_to_upper(data: list):
    new_data = []
    for todo in data:
        new_todo = {}
        for key, value in todo.items():
            new_todo[key] = value.upper() if isinstance(value, str) else value
        new_data.append(new_todo)
    return new_data


# роут, который извлекает и обрабатывает данные от внешнего API
@app.get("/todos")
async def get_and_process_todos():
    todos = fetch_todos()
    if todos:
        return data_values_to_upper(todos)
    else:
        return {"error": "Failed to fetch todos from the external API"}


if __name__ == '__main__':
    uvicorn.run('app.homeworks.homework_7_2:app', reload=True)

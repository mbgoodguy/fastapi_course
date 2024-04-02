from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()


class UserPayload(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    id: int


users_db: dict = {}


class UserNotExistExc(HTTPException):
    def __init__(self, errors=list[str]):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        self.errors = errors


class UserExists_409(HTTPException):
    def __init__(self, message: Optional[str | None] = None, errors=list[str]):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
        self.errors = errors


@app.exception_handler(UserNotExistExc)
def user_not_exist_404_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'detail': exc.detail,
            # 'errors': exc.errors
        }
    )


@app.exception_handler(UserExists_409)
def user_exists_409_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            # 'detail': exc.detail,
            'errors': exc.errors
        }
    )


def id_generator():
    counter = max(users_db.keys(), default=0) + 1
    while True:
        yield counter
        counter += 1


gen_id = id_generator()


def check_user_exists(username: str, email: str):
    errors = []
    for user in users_db.values():
        if username == user.username or email == user.email:
            errors.append('NOT UNIQUE USERNAME OR EMAIL')

    if errors:
        raise UserExists_409(errors=errors)


def check_user_get(pk: int):
    if pk not in users_db.keys():
        raise UserNotExistExc()


@app.get("/sum/")
async def calculate_sum(a: int, b: int):
    return {"result": a + b}


@app.post('/user', response_model=UserResponse)
async def add_user(user_data: UserPayload):
    check_user_exists(username=user_data.username, email=user_data.email)
    db_user = UserResponse(id=next(gen_id), username=user_data.username, email=user_data.email)

    users_db[db_user.id] = db_user
    print(db_user)

    return db_user


@app.get('/user/{pk}', response_model=UserResponse)
async def get_user(pk: int):
    check_user_get(pk=pk)

    return users_db[pk]


@app.delete('/user/{pk}')
async def delete_user(pk: int):
    check_user_get(pk)
    user = users_db[pk]
    print(user)

    deleted = users_db.pop(pk).id

    return JSONResponse(
        status_code=200,
        content=f'Deleted user with id {deleted} succesfully'
    )


@app.get('/users')
async def get_users():
    return users_db

if __name__ == "__main__":
    uvicorn.run('app.homeworks.homework_7_1:app', host="localhost", port=8000, reload=True)

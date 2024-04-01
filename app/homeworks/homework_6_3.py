import uvicorn

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from starlette.exceptions import HTTPException

app = FastAPI()


class UserPayload(BaseModel):
    username: str
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    username: str
    email: EmailStr


class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    errors: list[str]


users_db: dict[int, User] = {}


class NonExistingUserExc(HTTPException):
    def __init__(self, errors: list[str]):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.errors = errors


class InvalidUserPayloadExc(HTTPException):
    def __init__(self, errors: list[str], message: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user data")
        self.errors = errors
        self.message = message


@app.exception_handler(InvalidUserPayloadExc)
def invalid_user_payload_exc_handler(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'message': exc.message,
            'errors': exc.errors  # обращаемся к атрибуту errors класса исключения для получения ошибок
        }
    )


@app.exception_handler(NonExistingUserExc)
def non_existing_user_exc(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'errors': exc.errors  # обращаемся к атрибуту errors класса исключения для получения ошибок
        }
    )


def check_db_user(user: UserPayload):
    errors = []
    for db_user in users_db.values():
        if user.username == db_user.username:
            errors.append('Not unique username')
        if user.email == db_user.email:
            errors.append('Not unique email')

    if len(errors) > 0:
        raise InvalidUserPayloadExc(errors, message='Юзер с указанным email или username существует')


def get_user(pk: int):
    if pk not in users_db:
        errors = [f'User with id {pk} not found']
        raise NonExistingUserExc(errors=errors)
    return users_db[pk]


def id_generator() -> int:
    counter = max(users_db.keys()) if users_db else 0
    while True:
        counter += 1
        yield counter


id_gen = id_generator()


@app.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserPayload):
    check_db_user(user)
    db_user = User(
        id=next(id_gen),  # id=id_gen - приведет к ошибке. должен быть next(id_gen)
        username=user.username,
        email=user.email
    )
    users_db[db_user.id] = db_user

    return db_user


@app.get("/users/{user_id}", response_model=User)
async def read_user_by_id(pk: int):
    return get_user(pk)


if __name__ == "__main__":
    uvicorn.run('app.homeworks.homework_6_3:app', host="localhost", port=8000, reload=True)

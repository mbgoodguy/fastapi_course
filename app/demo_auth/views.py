import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

router = APIRouter(prefix='/demo_auth', tags=['Demo Auth'])  # роутер нужно подключить к приложению

security = HTTPBasic()


# @router.get('/basic_auth')
# def demo_basic_auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
#     # Annotated - для группировки нескольких аннотаций.
#     # HTTPBasic - класс который проверяет выполнен ли вход.
#     # HTTPBasicCredentials - указан для получения credentials. Нужно указать что будет их предоставлять.
#     # Depends(security) - говорим что security будет предоставлять данные аутентификации.
#     return {
#         'message': 'Hello!',
#         'username': credentials.username,
#         'password': credentials.password
#     }


# only for example
usernames_to_passwords = {
    'admin': 'admin',
    'John': 'john_pass',
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"}, # указываем что работаем с аутентификацией по Basic, чтобы браузер понял что можем залогиниться по BasicAuth
        # headers={"WWW-Authenticate": "LOL"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)

    if correct_password is None:
        raise unauthed_exc

    # проверки паролей и других важных данных лучше делать через secrets
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


# в это view не попадем если пользователь не найден или пароль неверный
@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }

import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, File, Header
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.responses import Response

router = APIRouter(prefix='/demo_auth', tags=['Demo Auth'])  # роутер нужно подключить к приложению

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
        credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
        # указываем что работаем с аутентификацией по Basic для отображения повторного приглашения для входа в систему
        # headers={"WWW-Authenticate": "LOL"},  # можем установить любой заголовок :)
    )
    correct_password = usernames_to_passwords.get(credentials.username)

    if correct_password is None:
        raise unauthed_exc

    # проверки паролей и других важных данных лучше делать через secrets, т.к усложняет атаки по времени
    # инфо: https://qapp.tech/help/timing-attack
    if not secrets.compare_digest(
            credentials.password.encode("utf-8"),
            correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


# в это view не попадем если пользователь не найден или пароль неверный
@router.get("/basic-auth-username")
def demo_basic_auth_username(
        auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }


#  python -c 'import secrets; print(secrets.token_hex())'  - получаем токен и разбиваем его на 2 части для примера
# static - потому что статичный, неизменяемый токен
static_auth_token_to_username = {
    '1781633e2c3894948edf403154caf238': 'admin',
    '3a30e60716ce55547a166c50f139e77a': 'john',
}


# помощник для получения данных юзера по статичному токену
def get_username_by_static_token(
        static_token: str = Header(alias='x-auth-token')
        # строка которую мы ждем получить из заголовков. alias - как ожидаем получить заголовок (любое строковое значение)
) -> str:
    if username := static_auth_token_to_username.get(
            static_token):  # walrus operator означает присвоить значение переменной и вернуть это значение.
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token invalid'
    )


@router.get("/auth_by_token")
def demo_auth_some_http_header(
        username: str = Depends(get_username_by_static_token),  # передан помощник
):
    return {
        "message": f"Hi, {username}!",
        "username": username,
    }


# Learn Access to Headers (recieving and sending)

# 1 вариант получения заголовков запросов. Параметр со значением по умолчанию
@router.get('/get_headers_w_default')
async def root(x_token: Annotated[str | None, Header()] = None):  # Header() - for getting
    return {'X-Token values': x_token}

# 2 вариант получения заголовков запросов. Параметр без значения по умолчанию -> обязательный
@router.get("/get_headers_wo_default")
def root(user_agent: str = Header()):
    return {"User-Agent": user_agent}


@router.get("/send_headers")
def root(response: Response):
    response.headers["Secret-Code"] = "123459"
    return {"message": "Hello from my api", 'headers': response.headers}

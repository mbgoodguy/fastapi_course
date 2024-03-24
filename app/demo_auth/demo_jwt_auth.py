from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from starlette import status

from demo_auth import utils as auth_utils
from demo_auth.exceptions import inactive_exc, unauthed_exc
from demo_auth.utils import decode_jwt
from schemas.base_models import UserSchema

router = APIRouter(prefix='/jwt')
# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/jwt/login')  # более простой способ автоматического получения токена без его ручного обновления


class Token(BaseModel):
    access_token: str
    token_type: str


john = UserSchema(
    username='john',
    password=auth_utils.hash_pwd('qwerty'),
    email='john@example.com'
)

sam = UserSchema(
    username='sam',
    password=auth_utils.hash_pwd('secret'),
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam
}


def validate_auth_user(username: str = Form(), password: str = Form()):
    #  pip install python-multipart необходимо для работы с Form()

    if not (user := users_db.get(
            username)):  # здесь присваиваем в переменную user юзера по username из users_db и сразу проверяем что он существует с помощью walrus operator
        raise unauthed_exc

    if not auth_utils.validate_pwd(pwd=password,
                                   hashed_pwd=user.password):  # проверка на совпадение паролей (сырого в виде строки и хешированного)
        raise unauthed_exc

    if not user.active:  # чтобы запретить доступ к функционалу юзерам, у которых active=False
        raise inactive_exc
    return user


# def get_curr_auth_user(token: str = Depends(http_bearer)) -> UserSchema:  # если оставить str - появится иконка авторизации по bearer
# т.к ф-ия вернула нам payload, то меняем ее сигнатуру
def get_curr_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        token: str = Depends(oauth2_scheme)  # получаем токен напрямую благодаря OAuth2PasswordBearer вместо HTTPBearer
) -> UserSchema:  # т.к ф-ия вернула нам payload, то меняем ее сигнатуру
    # print(token)  # scheme='Bearer' credentials='qwerty' - то что передается в запросе. Нам приходит структура HTTPCredentials
    # поэтому правильнее будет назвать параметр как credentials, а не token

    # token = credentials.credentials
    print(token)  # в терминале будет распечатан сам токен qwerty

    # Обработка ошибки jwt.exceptions.DecodeError: Not enough segments, которая возникает потому что в запросе
    # содержится qwerty, который мы(от лица клиента) указали в форме авторизации HTTPBearer. В swagger же выводится 500 ошибка.
    # При попытке распарсить этот qwerty с помощью decode_jwt и возникает ошибка, но на самом деле это не 500 ошибка,
    # т.к это проблема юзера что он указал неправильный токен qwerty. Поэтому мы ее и обрабатываем как InvalidTokenError
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token error: {e}'
        )

    return payload


def get_curr_auth_user(payload: dict = Depends(get_curr_token_payload)) -> UserSchema:
    # payload мы получаем из заголовка запроса (HTTPAuthorizationCredentials) в зависимости
    username: str | None = payload.get('sub')

    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token invalid (user not found)'
    )


# def get_curr_active_auth_user(user: UserSchema = Depends(get_curr_auth_user)):
def get_curr_active_auth_user(user: UserSchema = Depends(get_curr_auth_user)):
    if user.active:
        return user
    raise inactive_exc


@router.post('/login', response_model=Token)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        'sub': user.username,  # вместо username мог быть id
        'username': user.username,
        'email': user.email,
    }

    access_token = auth_utils.encode_jwt(payload=jwt_payload)

    return Token(access_token=access_token,
                 token_type='Bearer')  # Bearer - тип который по умочланию исп-ем для подобных токенов


@router.get('/me')
def auth_user_check_info(
        payload: dict = Depends(get_curr_token_payload),
        user: UserSchema = Depends(get_curr_active_auth_user)
):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat
    }

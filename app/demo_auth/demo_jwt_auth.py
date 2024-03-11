from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel
from starlette import status
from schemas.base_models import UserSchema
from demo_auth import utils as auth_utils

router = APIRouter(prefix='/jwt', tags=['JWT'])


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
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )
    if not (user := users_db.get(username)): # здесь присваиваем в переменную user юзера по username из users_db и сразу проверяем что он существует с помощью walrus operator
        raise unauthed_exc

    if not auth_utils.validate_pwd(pwd=password, hashed_pwd=user.password):  # проверка на совпадение паролей (сырого в виде строки и хешированного)
        raise unauthed_exc

    if not user.active:  # чтобы запретить доступ к функционалу юзерам, у которых active=False
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User inactive'
        )
    return user


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

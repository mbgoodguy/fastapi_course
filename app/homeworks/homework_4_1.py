from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette import status

router = APIRouter(prefix='/homeworks', tags=['Homeworks'])
security = HTTPBasic()


class User(BaseModel):
    username: str
    password: str

USER_DATA = [User(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]

def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user

    return None



def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)

    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Basic'} # чтобы видеть повторно приглашение для авторизации которое можно убрать только если нажать cancel
        )
    return {'mesg': 'You got my secret, welcome'}


@router.get('/protected_resource')
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}



from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix='/demo_auth', tags=['Demo Auth'])  # роутер нужно подключить к приложению

security = HTTPBasic()


@router.get('/basic_auth')
def demo_basic_auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    # Annotated - для группировки нескольких аннотаций.
    # HTTPBasic - класс который проверяет выполнен ли вход.
    # HTTPBasicCredentials - указан для получения credentials. Нужно указать что будет их предоставлять.
    # Depends(security) - говорим что security будет предоставлять данные аутентификации.
    return {
        'message': 'Hello!',
        'username': credentials.username,
        'password': credentials.password
    }

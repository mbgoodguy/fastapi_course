import uuid
from datetime import datetime
from typing import Any

import uvicorn

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Cookie, Form
from fastapi import Cookie
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.responses import Response
from app.schemas.base_models import AuthUser
from app import router as router_v1
from core.config import settings

# -- перенесены в __init__.py для включения --
# from app.views.products_views import router as products_router
# from app.demo_auth.views import router as demo_auth_router


app = FastAPI()
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)  # подключение роутера из __init__.py к главному роутеру


feedbacks = []
users = []
COOKIES: dict[str, dict[str, Any]] = {}

fake_auth_user: dict = {"username": "user@example.com", "password": "qqq"}
fake_auth_users: list[AuthUser] = [AuthUser(**fake_auth_user)]


# login_by_cookies
@app.post('/login_cookie')
async def login(response: Response, user_data: AuthUser):
    for fu in fake_auth_users:
        if fu.username == user_data.username and fu.password == user_data.password:
            # session_token = f'{uuid.uuid4()}'  # does not work if not str.
            session_token = f'{uuid.uuid4().hex}'  # for values without '-'
            COOKIES[session_token] = user_data
            response.set_cookie(key='session_token', value=session_token, httponly=True)
            COOKIES['login_at']= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f'Session token: {session_token}')
            print(user_data, type(user_data))
            print(f'Fake auth users list: {fake_auth_users}')
            print(f'COOKIES dict: {COOKIES}')
            return {'message': 'cookies has been set'}
    return {'message': 'ERROR! cookies has NOT been set'}


@app.get("/get_cookie")
async def get_cookies(session_token=Cookie()):
    user = COOKIES.get(session_token)
    if user:
        return user.model_dump()  # in pydantic v1 it was dict()
    else:
        return {'message': 'Unauthorized'}


if __name__ == '__main__':
    uvicorn.run("app.main:app", reload=True)

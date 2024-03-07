import uuid
from typing import Annotated

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Cookie, Form
from fastapi.responses import FileResponse
from fastapi import Cookie
from pydantic import PositiveInt, EmailStr
from starlette.responses import Response

from app.fakes.fake_databases import generate_fake_users_db, generate_fake_products
from app.views.products_views import router as products_router
from schemas.base_models import AuthUser

app = FastAPI()
app.include_router(products_router)  # подключен --> можем пользоваться

feedbacks = []
users = []
sessions = {}

fake_auth_user: dict = {"username": "user@example.com", "password": "qqq"}
fake_auth_users: list[AuthUser] = [AuthUser(**fake_auth_user)]


@app.post('/login')
async def login(response: Response, user_data: AuthUser):
    for fu in fake_auth_users:
        if fu.username == user_data.username and fu.password == user_data.password:
            session_token = f'{uuid.uuid4()}'  # does not work if not str
            sessions[session_token] = user_data
            response.set_cookie(key='session_token', value=session_token, httponly=True)
            print(session_token)
            print(user_data, type(user_data))
            print(fake_auth_users)
            print(sessions)
            return {'message': 'cookies has been set'}
    return {'message': 'ERROR! cookies has NOT been set'}


@app.get("/cookie")
async def get_cookies(session_token=Cookie()):
    user = sessions.get(session_token)
    if user:
        return user.model_dump()  # in pydantic v1 it was dict()
    else:
        return {'message': 'Unauthorized'}


if __name__ == '__main__':
    uvicorn.run("app.main:app", reload=True)

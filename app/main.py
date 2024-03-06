import uuid
from typing import Annotated

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Cookie, Form
from fastapi.responses import FileResponse
from fastapi import Cookie
from pydantic import PositiveInt, EmailStr
from starlette.responses import Response

from app.fakes.fake_databases import generate_fake_users_db, generate_fake_products
from app.models.base_models import Feedback, Item, UserCreate, Product, AuthUser

app = FastAPI()

feedbacks = []
users = []
sessions = {}

fake_db = generate_fake_users_db(30)
products_db = generate_fake_products(100)

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

# @app.get('/users/{user_id}')
# def get_user_by_id(user_id: int):
#     merged_fake_data = {k: v for user_dict in fake_db for k, v in user_dict.items()}
#     print(merged_fake_data)
#     if user_id in merged_fake_data:
#         return {'user_id': user_id, 'user_name': merged_fake_data[user_id]}
#     else:
#         return {'error': f'No such user with id {user_id}'}
#
#
# @app.get('/fake_users')
# def get_fake_users(limit: int = 5):
#     return fake_db[:limit]
#
#
# @app.post('/feedback')
# def feedback_handler(feedback: Feedback):
#     feedbacks.append(feedback.message)
#     return {'message': f'Feedback received. Thank you, {feedback.name}'}
#
#
# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file), "filename": file.filename}
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}
#
#
# @app.get('/download_file')
# async def download_file():
#     return FileResponse(path='q.txt', filename='your_file.txt', media_type='multipart/form-data')
#
#
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_db[skip: skip + limit]
#
#
# @app.get('/items/')
# async def create_item(item: Item):
#     return item
#
#
# @app.post('/create_user')
# async def create_user(user: UserCreate):
#     users.append(user)
#     return user
#
#
# @app.get('/users')
# async def get_users():
#     return users

# @app.get('/products')
# async def get_products():
#     return products_db
#
#
# @app.get('/product/{product_id}')
# async def get_product(product_id: int):
#     for product_dict in products_db:
#         if product_dict['product_id'] == product_id:
#             return product_dict
#     raise HTTPException(detail=f'No product with id {product_id}', status_code=400)
#
#
# @app.get('/products/search')
# async def search_products(keyword: str, category: str = None, limit: int = 10):
#     res = []
#
#     for product_dict in products_db:
#         product_name = product_dict['name']
#         product_category = product_dict['category']
#         if keyword.lower() in product_name.lower() or product_category == category:
#             res.append(product_dict)
#
#     if not res:
#         raise HTTPException(detail=f'No products with "{keyword}" in name', status_code=404)
#     print(len(res))
#     return res[:limit]

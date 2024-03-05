from typing import Annotated

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import PositiveInt

from app.fakes.fake_databases import generate_fake_users_db, generate_fake_products
from app.models.base_models import Feedback, Item, UserCreate, Product

app = FastAPI()

fake_db = generate_fake_users_db(30)

feedbacks = []
users = []
products_db = generate_fake_products(100)


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

@app.get('/products')
async def get_products():
    return products_db


@app.get('/product/{product_id}')
async def get_product(product_id: int):
    for product_dict in products_db:
        if product_dict['product_id'] == product_id:
            return product_dict
    raise HTTPException(detail=f'No product with id {product_id}', status_code=400)


@app.get('/products/search')
async def search_products(keyword: str, category: str = None, limit: int = 10):
    res = []

    for product_dict in products_db:
        product_name = product_dict['name']
        product_category = product_dict['category']
        if keyword.lower() in product_name.lower() or product_category == category:
            res.append(product_dict)

    if not res:
        raise HTTPException(detail=f'No products with "{keyword}" in name', status_code=404)
    print(len(res))
    return res[:limit]

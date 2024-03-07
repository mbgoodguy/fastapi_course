from fastapi import APIRouter, HTTPException

from app.fakes.fake_databases import generate_fake_products, generate_fake_users_db

router = APIRouter(prefix='/products', tags=['ABOBA'])  # нужно подключить в основной

fake_db = generate_fake_users_db(30)
products_db = generate_fake_products(100)


@router.get('/')
async def get_products():
    return products_db


# порядок важен. Если указать после @router.get('/{product_id}') будет ошибка
@router.get('/search')
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


@router.get('/{product_id}')
async def get_product(product_id: int):
    for product_dict in products_db:
        if product_dict['product_id'] == product_id:
            return product_dict
    raise HTTPException(detail=f'No product with id {product_id}', status_code=400)

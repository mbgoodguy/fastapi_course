from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter(prefix='/homeworks', tags=['Homeworks'])

# можно объявить функцию для проверки наличия перечисленных заголовков в входящих заголовках
def is_headers(headers: Request.headers):
    headers_tuple = ('User-Agent', 'Accept-Language')

    for header in headers_tuple:
        if header not in headers:
            raise HTTPException(status_code=400, detail='Missing required headers')

    print('Correct headers')


@router.get('/get')
def get_headers(request: Request):
    is_headers(request.headers)

    response_data = {
        "User-Agent": request.headers.get('user-agent'),
        "Accept-Language": request.headers.get('accept-language')
    }

    return response_data

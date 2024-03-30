from typing import Optional

from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, Field, conint, constr
from starlette.requests import Request
from starlette.responses import JSONResponse

from schemas.base_models import User

router = APIRouter(prefix='/homeworks/6_2', tags=['Homeworks'])


# def request_validation_handler(request: Request, exc: Exception):
#     errors = [error.get('msg') for error in exc.errors()]
#     return JSONResponse(status_code=400, content={'errors': errors})


class Data(BaseModel):
    name: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

@router.post('/user')
def get_user(data: Data):
    return data.model_dump_json()

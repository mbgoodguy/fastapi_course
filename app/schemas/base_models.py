from datetime import datetime
from typing import Union, List, Optional

from fastapi import Body
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    user_id: int
    username: str
    age: int
    first_name: str
    middle_name: str
    last_name: str


class Feedback(BaseModel):
    name: str = Field(max_length=5)
    message: str = Field(max_length=5)


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(default=None, lt=100)
    is_subscribed: bool = False


class Product(BaseModel):
    product_id: int = Field(default=1, ge=1)
    name: str
    category: str
    price: float = Field()


class AuthUser(BaseModel):
    username: EmailStr
    password: str

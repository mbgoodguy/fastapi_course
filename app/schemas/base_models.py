from datetime import datetime
from pathlib import Path
from typing import Union, List, Optional

from fastapi import Body
from pydantic import BaseModel, Field, EmailStr, ConfigDict

BASE_DIR = Path(__file__).parent.parent

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


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes  # need bcrypt lib for encrypting password
    email: EmailStr | None = None
    active: bool = True
    # ConfigDict чтобы точно передать типы которые нам нужны и не конвертировались из одного в другой.
    # strict - строгое указание типов. # https://docs.pydantic.dev/latest/concepts/strict_mode/#strict-mode-with-configdict

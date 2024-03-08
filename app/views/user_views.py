from collections import OrderedDict

from fastapi import APIRouter, Depends, HTTPException

from dependencies import AuthGuard, Paginator
from fakes.fake_databases import generate_fake_users_db
from schemas.base_models import User

router = APIRouter(prefix='/users', tags=['Users'])

# define global dependency for this router. It means that dependecies in list will apply for all endpoints in this router (that has prefix 'users')
# router = APIRouter(prefix='/users', tags=['Users'], dependencies=[Depends(AuthGuard('users')),])

fake_users_db = generate_fake_users_db(30)


# @router.get('/')
# async def get_fake_users(limit: int = 5):
#     return fake_users_db[:limit]


@router.get('/users_by_auth_guard_w_pagination')
async def get_fake_users(pagination_params: Paginator = Depends(Paginator)):
    return fake_users_db[pagination_params.skip: pagination_params.limit + pagination_params.skip]


@router.get('/users_by_auth_guard', dependencies=[Depends(AuthGuard('users'))])  # так мы не захламляем нашу функцию параметрами которые не используются в ней
async def get_fake_users():
    return fake_users_db

@router.post('/create')
async def create_user(user: User):
    fake_users_db.append(user)
    print(fake_users_db)
    return user


@router.get('/{user_id}')
def get_user_by_id(user_id: int):
    for user_dict in fake_users_db:
        if user_dict['user_id'] == user_id:
            return user_dict
    else:
        return {'error': f'Пользователь с ID {user_id} не найден'}

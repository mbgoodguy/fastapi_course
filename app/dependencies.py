# first variant of dependency define
from fastapi import HTTPException
from starlette.requests import Request




# def get_pagination_params(limit: int = 10, skip: int = 0):
#     return {'limit': limit, 'skip': skip}
#

# # second variant of dependency define as class
class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip


class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        if 'admin_cookie' not in request.cookies:
            raise HTTPException(
                status_code=403,
                detail='Запрещено'
            )
        # check that info about user rights in cookies
        return True


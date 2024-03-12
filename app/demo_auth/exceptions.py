from fastapi import HTTPException
from starlette import status

unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid username or password'
)

inactive_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='User inactive'
)

unauthed_basic_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers={"WWW-Authenticate": "Basic"}
    # указываем что работаем с аутентификацией по Basic для отображения повторного приглашения для входа в систему
    # headers={"WWW-Authenticate": "LOL"},  # можем установить любой заголовок :)
)

invalid_token_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token invalid'
)


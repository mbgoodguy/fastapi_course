import bcrypt
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from sqlalchemy import create_engine, Integer, String, CheckConstraint, insert, Column, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from db.config import settings

app = FastAPI()
engine = create_engine(url=settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
security = HTTPBasic()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=20), unique=True, index=True)
    age = Column(Integer(), CheckConstraint('age > 0 and age < 100'))
    # password = Column(String())


class UserPayload(BaseModel):
    username: str
    age: int


class UserOutput(BaseModel):
    id: int
    username: str
    age: int


# class UserCredentials(BaseModel):
#     username: str
#     password:


class UsersRepository:
    @classmethod
    def add(cls, db: Session, values: dict):
        stmt = insert(User).values(**values).returning(User)
        new_user = db.execute(stmt)
        db.commit()
        return new_user.scalar_one()

    @classmethod
    def get_by_pk(cls, db: Session, pk: int):
        user = db.get(User, pk)
        return user

    @classmethod
    def get_all(cls, db: Session):
        query = text('SELECT * FROM "user"')
        res = db.execute(query)

        # Convert tuples to dictionaries using list comprehension
        users = [{'id': row[0], 'username': row[1], 'age': row[2]} for row in res]
        return users


class UserService:
    @classmethod
    def add(cls, db: Session, user: UserPayload):
        new_user = UsersRepository.add(db, user.model_dump())
        return new_user

    @classmethod
    def get(cls, db: Session, pk: int):
        user = UsersRepository.get_by_pk(db, pk)
        return user

    @classmethod
    def get_all(cls, db: Session):
        users = UsersRepository.get_all(db)
        return users


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_pwd(pwd: str):
    salt = bcrypt.gensalt()
    pwd_bytes = pwd.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def get_user_from_db(db: Session, pk: int):
    user = UserService.get(db, pk)

    if user:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail=f'User with id {pk} not exists'
        )


@app.post('/user')
def create_user(data: UserPayload, db: Session = Depends(get_db)):
    try:
        UserService.add(db=db, user=data)
        return data
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.get('/users')
def get_users(db: Session = Depends(get_db)):
    users = UserService.get_all(db)
    return users


# @app.post('/login')
# def login(creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
#     UsersRepository.get_all(db)


if __name__ == '__main__':
    uvicorn.run('app.homeworks.homework_7_3:app', reload=True)

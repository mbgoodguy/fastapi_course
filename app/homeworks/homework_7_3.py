from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Integer, String, CheckConstraint, insert, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from db.config import settings

app = FastAPI()
engine = create_engine(url=settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=20), unique=True, index=True)
    age = Column(Integer(), CheckConstraint('age > 0 and age < 100'))


class UsersRepository:
    @classmethod
    def add(cls, db: Session, values: dict):
        stmt = insert(User).values(**values).returning(User)
        new_user = db.execute(stmt)
        db.commit()
        return new_user.scalar_one()

class UserPayload(BaseModel):
    username: str
    age: int

class UserService:
    @classmethod
    def add(cls, db: Session, user: UserPayload):
        new_user = UsersRepository.add(db, user.model_dump())
        return new_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


if __name__ == '__main__':
    uvicorn.run('app.homeworks.homework_7_3:app', reload=True)

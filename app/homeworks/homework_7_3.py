import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Integer, String, CheckConstraint
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

from db.config import settings

app = FastAPI()
engine = create_engine(url=settings.DB_URL)
session = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    username: Mapped[str] = mapped_column(String(length=20), unique=True)
    age: Mapped[int] = mapped_column(Integer(), CheckConstraint('age > 0 and age < 100'))


def get_db():
    with session() as db:
        yield db


class UserPayload(BaseModel):
    username: str
    age: int


@app.post('/user')
def create_user(data: UserPayload, db: Session = Depends(get_db)):
    db.add(data)
    db.commit()


if __name__ == '__main__':
    uvicorn.run('app.homework_7_3:app', reload=True)

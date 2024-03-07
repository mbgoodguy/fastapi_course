from fastapi import APIRouter
from app.demo_auth.views import router as demo_auth_router

router = APIRouter()
router.include_router(router=demo_auth_router)  # префикс не указываем т.к он уже указан в самом роутере

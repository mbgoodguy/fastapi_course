if __name__ == '__main__':
    from fastapi import APIRouter
    from app.views.products_views import router as products_router
    from app.views.user_views import router as users_router

    from app.demo_auth.views import router as demo_auth_router
    from app.demo_auth.demo_jwt_auth import router as jwt_router

    from app.homeworks.homework_3_3 import router as homework_3_3_router
    from app.homeworks.homework_4_1 import router as homework_4_1_router
    from app.homeworks.homework_6_2 import router as homework_6_2_router

    router = APIRouter()  # подключить в main.py

    router.include_router(router=demo_auth_router)  # префикс не указываем т.к он уже указан в самом роутере
    router.include_router(router=products_router)
    router.include_router(router=users_router)
    router.include_router(router=jwt_router)

    router.include_router(router=homework_3_3_router)
    router.include_router(router=homework_4_1_router)
    router.include_router(router=homework_6_2_router)



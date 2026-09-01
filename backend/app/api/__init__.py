from fastapi import APIRouter
from app.api.admin_users import router as admin_user_router


router = APIRouter(prefix='/api/auths')


router.include_router(admin_user_router)



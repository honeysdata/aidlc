# Admin API Routers
from fastapi import APIRouter
from app.routers.admin import auth, order, table, menu, category

router = APIRouter(prefix="/admin")
router.include_router(auth.router)
router.include_router(order.router)
router.include_router(table.router)
router.include_router(menu.router)
router.include_router(category.router)

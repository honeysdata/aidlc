# Customer API Routers
from fastapi import APIRouter
from app.routers.customer import auth, menu, order

router = APIRouter(prefix="/customer")
router.include_router(auth.router)
router.include_router(menu.router)
router.include_router(order.router)

# API Routers
from fastapi import APIRouter
from app.routers.customer import router as customer_router
from app.routers.admin import router as admin_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(customer_router)
api_router.include_router(admin_router)

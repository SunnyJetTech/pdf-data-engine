from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings 
from routers import user_router
from db.database import create_tables
from db.mongo_db import mongo_db
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("app")

app = FastAPI(
    title="E-commerce web application",
    description="Cosmetics Online shopping",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True,
)
# 54, 41 room door and entrance 52'

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )
    

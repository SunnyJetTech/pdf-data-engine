from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings 
from routers import admin_router, document_router, payment_router, pdf_router, quota_router, subscription_router, user_router
from db.database import create_tables
from db.mongo_db import mongodb
import logging
from core.exceptions import value_error_handler, generic_exception_handler
from contextlib import asynccontextmanager
from middleware.gzip import register_gzip
from middleware.timeout import TimeoutMiddleware
from middleware.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    create_tables()

    yield

    logger.info("Shutting down application...")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)
app = FastAPI(
    title="PDF Search API",
    description="Search, filter, export and manage PDF data.",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    debug=True,
    lifespan=lifespan
)

register_gzip(app)

app.add_middleware(
    TimeoutMiddleware,
    timeout=7200,
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(
    ValueError,
    value_error_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

routers = [
    user_router.router,
    document_router.router,
    pdf_router.router,
    admin_router.router,
    payment_router.router,
    quota_router.router,
    subscription_router.router,
]

for router in routers:
    app.include_router(router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=logging.INFO,
    )
    

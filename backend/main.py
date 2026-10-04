import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.config import settings
from core.exceptions import generic_exception_handler, value_error_handler
from middleware.gzip import register_gzip
from middleware.rate_limit import limiter
from middleware.timeout import TimeoutMiddleware
from routers import admin_router, document_router, payment_router, pdf_router, quota_router, subscription_router, user_router,

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Starting %s in %s environment",
        settings.APP_NAME,
        settings.ENVIRONMENT,
    )

    yield

    logger.info("Shutting down %s", settings.APP_NAME)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title=settings.APP_NAME,
    description="A multi-tenant data platform for PDF reports, search, analytics, exports, and external integrations.",
    version=settings.API_VERSION,
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_gzip(app)

app.add_middleware(
    TimeoutMiddleware,
    timeout=120,
)

if settings.RATE_LIMIT_ENABLED:
    app.state.limiter = limiter

    app.add_exception_handler(RateLimitExceeded,  _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

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

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=not settings.is_production, log_level="info")
    
    
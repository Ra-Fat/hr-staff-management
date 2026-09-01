from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import close_db, init_db
from app.api import router as v1_router


from app.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(settings.DATABASE_URL)
    yield
    await close_db()

_is_production = settings.ENVIRONMENT.lower() == "production"


app = FastAPI(
    title='HR Staff Management API',
    docs_url=None if _is_production else "/docs",
    redoc_url=None if _is_production else "/redoc",
    openapi_url=None if _is_production else "/openapi.json",
    lifespan=lifespan
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    # Credentials must never be combined with a wildcard origin.
    allow_credentials="*" not in settings.ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Language",
        "X-Request-ID",
    ],
)


# --- Exception handlers ---

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# --- Routes ---

app.include_router(v1_router)

@app.get('/health', tags= ['Health'])
def health():
    return {'status': 'ok'}
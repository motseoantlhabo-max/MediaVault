from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import engine
from app.core.exception_handlers import (
    not_found_exception_handler,
    unauthorized_exception_handler,
    forbidden_exception_handler,
    bad_request_exception_handler,
    file_validation_exception_handler
)
from app.core.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    BadRequestException,
    FileValidationException
)
from app.api.v1.auth.router import router as auth_router
from app.api.v1.assets.router import router as assets_router
from app.api.v1.users.router import router as users_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="MediaVault Enterprise Processing Pipeline - Multi-tenant digital asset management engine"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(FileValidationException, file_validation_exception_handler)

# API routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(assets_router, prefix="/api/v1/assets", tags=["Assets"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    from app.core.database import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "MediaVault Enterprise Processing Pipeline API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

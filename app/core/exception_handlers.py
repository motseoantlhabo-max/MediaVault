from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    BadRequestException,
    FileValidationException
)


async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail}
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Bearer"}
    )


async def forbidden_exception_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail}
    )


async def bad_request_exception_handler(request: Request, exc: BadRequestException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail}
    )


async def file_validation_exception_handler(request: Request, exc: FileValidationException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={"detail": exc.detail}
    )

from fastapi import HTTPException, status


class MediaVaultException(HTTPException):
    """Base exception for MediaVault application."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(MediaVaultException):
    """Resource not found exception."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(MediaVaultException):
    """Unauthorized access exception."""
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(MediaVaultException):
    """Forbidden access exception."""
    def __init__(self, detail: str = "Forbidden access"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestException(MediaVaultException):
    """Bad request exception."""
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class FileValidationException(MediaVaultException):
    """File validation exception."""
    def __init__(self, detail: str = "File validation failed"):
        super().__init__(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=detail)

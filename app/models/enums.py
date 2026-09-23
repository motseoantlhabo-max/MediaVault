from enum import Enum


class UserRole(str, Enum):
    SUPERADMIN = "superadmin"
    CREATOR = "creator"
    VIEWER = "viewer"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

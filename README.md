# MediaVault Enterprise Processing Pipeline

A high-performance, production-ready RESTful API for multi-tenant digital asset management. MediaVault enables enterprises to securely upload, index, extract, and search through media files (images and scanned documents) with OCR capabilities and fine-grained role-based access control.

## Features

- **Security & Authentication**
  - OAuth2 Password flow with JWT Access & Refresh tokens
  - Argon2 password hashing
  - Role-Based Access Control (RBAC) with three user tiers:
    - SuperAdmin: Unrestricted system access
    - Creator: Upload, edit, and delete owned assets
    - Viewer: Read-only access to assets

- **File Processing**
  - Multipart file uploads (JPG, PNG, PDF) with size limits (≤15MB)
  - MIME-type validation
  - Background OCR text extraction using Tesseract
  - Thumbnail generation for images
  - Real-time processing state tracking (PENDING, PROCESSING, COMPLETED, FAILED)

- **Database**
  - SQLAlchemy 2.0 with async engine
  - SQLite support (easily switchable to PostgreSQL)
  - Comprehensive relational schema with proper cascading deletes

- **API Design**
  - FastAPI with async support
  - Pydantic V2 schemas for validation
  - Custom exception handlers
  - OpenAPI documentation (Swagger UI)
  - File streaming with range header support

## Project Structure

```
MediaVault/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth/         # Authentication endpoints
│   │       ├── assets/       # Media asset management
│   │       └── users/        # User management (SuperAdmin)
│   ├── core/
│   │   ├── config.py         # Application configuration
│   │   ├── database.py       # Database connection and session
│   │   ├── dependencies.py   # FastAPI dependencies (auth, RBAC)
│   │   ├── asset_dependencies.py  # Asset ownership checks
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── exception_handlers.py  # Exception handlers
│   ├── models/
│   │   ├── user.py           # User model
│   │   ├── media_asset.py    # MediaAsset model
│   │   ├── tag.py            # Tag model
│   │   ├── asset_tag.py      # Asset-Tag join table
│   │   ├── asset_comment.py  # Comment model
│   │   ├── audit_log.py      # Audit log model
│   │   └── enums.py          # Enum definitions
│   ├── schemas/
│   │   ├── user.py           # User schemas
│   │   ├── media_asset.py    # MediaAsset schemas
│   │   ├── comment.py        # Comment schemas
│   │   └── tag.py            # Tag schemas
│   ├── services/
│   │   ├── auth_service.py   # Authentication logic
│   │   ├── asset_service.py  # Asset business logic
│   │   ├── file_service.py   # File operations
│   │   └── ocr_service.py    # OCR processing
│   ├── utils/
│   │   └── security.py       # Security utilities (JWT, password hashing)
│   └── main.py               # FastAPI application
├── alembic/
│   ├── versions/             # Migration scripts
│   ├── env.py                # Alembic environment
│   └── script.py.mako        # Migration template
├── uploads/                  # Uploaded files directory
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── alembic.ini              # Alembic configuration
└── README.md                # This file
```

## Installation

### Prerequisites

- Python 3.10-3.13 (Python 3.14 has compatibility issues with pydantic-core and requires Visual Studio C++ build tools)
- Tesseract OCR (for text extraction)
- Virtual environment

**Important Note:** Python 3.14 is not recommended for this project due to pydantic-core compilation issues. If you must use Python 3.14, you'll need to install Visual Studio Build Tools with C++ support.

### Setup

1. Clone the repository and navigate to the project directory:
```bash
cd MediaVault
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables (edit `.env` file):
```env
APP_NAME=MediaVault
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite+aiosqlite:///./mediavault.db
MAX_FILE_SIZE_MB=15
UPLOAD_DIR=uploads
TESSERACT_CMD=/usr/bin/tesseract  # Optional: Path to Tesseract executable
```

5. Initialize the database:
```bash
# The database will be automatically created on startup
# Or use Alembic for migrations:
alembic upgrade head
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user (default role: Creator)
- `POST /api/v1/auth/login` - Authenticate and receive JWT tokens

### Assets

- `POST /api/v1/assets/upload` - Upload a media file (Creator/Admin)
- `GET /api/v1/assets` - List assets with filtering and pagination (Authenticated)
- `GET /api/v1/assets/{id}` - Get asset details including OCR text (Authenticated)
- `GET /api/v1/assets/{id}/stream` - Stream file content (Owner/Admin)
- `DELETE /api/v1/assets/{id}` - Delete asset and file (Owner/Admin)
- `POST /api/v1/assets/{id}/comments` - Add comment to asset (Authenticated)

### Users (SuperAdmin only)

- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get specific user
- `PATCH /api/v1/users/{id}` - Update user

## Usage Examples

### Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "role": "creator"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Upload a File

```bash
curl -X POST "http://localhost:8000/api/v1/assets/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "title=My Image"
```

### List Assets

```bash
curl -X GET "http://localhost:8000/api/v1/assets?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Schema

### Users
- `id` (UUID, PK)
- `email` (Unique)
- `hashed_password`
- `role` (Enum: superadmin, creator, viewer)
- `is_active` (Boolean)

### MediaAssets
- `id` (UUID, PK)
- `title`
- `file_path`
- `mime_type`
- `ocr_text` (Optional)
- `status` (Enum: pending, processing, completed, failed)
- `owner_id` (FK → Users)

### Tags
- `id` (UUID, PK)
- `name` (Unique)

### AssetComments
- `id` (UUID, PK)
- `content`
- `asset_id` (FK → MediaAssets)
- `user_id` (FK → Users)

### AuditLogs
- `id` (UUID, PK)
- `action`
- `resource_type`
- `resource_id`
- `details` (Optional)
- `user_id` (FK → Users)
- `created_at` (DateTime)

## Security Features

- **Password Hashing**: Argon2 for secure password storage
- **JWT Tokens**: Access tokens (30min) and refresh tokens (7 days)
- **RBAC**: Three-tier role system with dynamic permission checking
- **Asset Ownership**: Dynamic dependency injection for resource access control
- **File Validation**: Size limits and MIME-type checking
- **CORS**: Configurable cross-origin resource sharing

## Background Processing

File uploads trigger background tasks for:
- OCR text extraction from images and PDFs
- Thumbnail generation for images
- Status updates (PENDING → PROCESSING → COMPLETED/FAILED)

## Testing

Run tests (if test suite is implemented):

```bash
pytest
```

## Development

### Adding New Migrations

```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Code Style

The project follows Python best practices with:
- Type hints throughout
- Async/await patterns
- Clean separation of concerns (models, schemas, services, API)
- Comprehensive error handling

## Production Considerations

- Change `SECRET_KEY` to a strong random value
- Set `DEBUG=False`
- Use PostgreSQL instead of SQLite for production
- Configure proper CORS origins
- Set up proper file storage (S3, etc.)
- Implement rate limiting
- Add monitoring and logging
- Use HTTPS

## License

This project is part of the MediaVault Intern Technical Assessment.

## Author

Motseoa - Backend Engineering Assessment
# MediaVault

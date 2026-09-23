try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Warning: pytesseract or PIL not available. OCR functionality will be disabled.")

import aiofiles
from pathlib import Path
from typing import Optional
from app.core.config import get_settings

settings = get_settings()

if TESSERACT_AVAILABLE and settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


async def extract_text_from_image(image_path: str) -> Optional[str]:
    if not TESSERACT_AVAILABLE:
        print("OCR not available: pytesseract or PIL not installed")
        return None
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip() if text else None
    except Exception as e:
        print(f"OCR Error: {e}")
        return None


async def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    if not TESSERACT_AVAILABLE:
        print("OCR not available: pytesseract or PIL not installed")
        return None
    
    try:
        # For PDF processing, we'd typically use pdf2image first
        # For simplicity, we'll skip PDF OCR in this implementation
        # or use a library like pdf2image + pytesseract
        return None
    except Exception as e:
        print(f"PDF OCR Error: {e}")
        return None


async def generate_thumbnail(image_path: str, thumbnail_path: str, size: tuple = (150, 150)) -> bool:
    if not TESSERACT_AVAILABLE:
        print("Thumbnail generation not available: PIL not installed")
        return False
    
    try:
        image = Image.open(image_path)
        image.thumbnail(size)
        image.save(thumbnail_path)
        return True
    except Exception as e:
        print(f"Thumbnail generation error: {e}")
        return False

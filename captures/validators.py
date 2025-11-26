"""
File upload validators for the captures app.

Multi-layer validation to prevent malicious uploads:
1. File size validation
2. Extension validation
3. MIME type validation (magic bytes)
4. Image integrity validation (Pillow)
"""
import os
import magic
from PIL import Image
from django.core.exceptions import ValidationError
from django.conf import settings


# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

# Allowed file extensions
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# Allowed MIME types (must match actual file content)
ALLOWED_MIME_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp'
]


def validate_image_file(file):
    """
    Multi-layer validation for uploaded image files.

    Validates:
    1. File size (max 10MB)
    2. File extension (jpg, jpeg, png, gif, webp)
    3. MIME type via magic bytes (not just extension)
    4. Image integrity (can be opened and verified by Pillow)

    Args:
        file: Django UploadedFile object

    Raises:
        ValidationError: If validation fails at any layer
    """

    # Layer 1: File size validation
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(
            f'Image file too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB. '
            f'Your file is {file.size // (1024*1024)}MB.'
        )

    # Layer 2: Extension validation
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f'Unsupported file extension: {ext}. '
            f'Allowed extensions: {", ".join(ALLOWED_EXTENSIONS)}'
        )

    # Layer 3: MIME type validation (magic bytes)
    # Read first 1KB to detect file type
    file_start = file.read(1024)
    file.seek(0)  # Reset file pointer for later reading

    mime_type = magic.from_buffer(file_start, mime=True)

    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValidationError(
            f'Invalid file type. File appears to be {mime_type}, '
            f'but only image files are allowed.'
        )

    # Layer 4: Image integrity validation
    # Try to open and verify the image with Pillow
    try:
        img = Image.open(file)
        img.verify()  # Verify it's actually an image
        file.seek(0)  # Reset file pointer again
    except Exception as e:
        raise ValidationError(
            f'Invalid or corrupted image file. Error: {str(e)}'
        )

    # Additional check: Image dimensions (optional safety check)
    # Reopen image to get dimensions (verify() closes the file)
    try:
        img = Image.open(file)
        width, height = img.size
        file.seek(0)  # Reset file pointer

        # Sanity check: reject extremely large images (potential decompression bomb)
        MAX_PIXELS = 50_000_000  # 50 megapixels
        if width * height > MAX_PIXELS:
            raise ValidationError(
                f'Image dimensions too large ({width}x{height} = {width*height:,} pixels). '
                f'Maximum is {MAX_PIXELS:,} pixels.'
            )
    except ValidationError:
        raise  # Re-raise our validation error
    except Exception as e:
        raise ValidationError(
            f'Cannot read image dimensions. Error: {str(e)}'
        )


def validate_file_size(file):
    """
    Validate file size is under the limit.

    Standalone validator for use in serializer field validation.
    """
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(
            f'File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB.'
        )


def validate_image_extension(file):
    """
    Validate file has an allowed image extension.

    Standalone validator for use in serializer field validation.
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f'Unsupported file extension: {ext}. '
            f'Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
        )

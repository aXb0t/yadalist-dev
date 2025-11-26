# Captures API Documentation

## Authentication

All endpoints require authentication using either:
- **Basic Auth**: `-u username:password`
- **Session Auth**: Django session cookie

## Base URL

```
/api/captures/items/
```

---

## Endpoints

### Create Capture

**POST** `/api/captures/items/`

Creates an empty capture item owned by the authenticated user.

**Request:**
```bash
http POST :8000/api/captures/items/ -a username:password
```

**Response:** `201 Created`
```json
{
    "id": 1,
    "short_uuid": "Exh4RVhahEtkQtxhKWEngr",
    "created_at": "2025-11-26T16:08:24.710130Z",
    "voice_transcript": "",
    "is_complete": false,
    "images": []
}
```

---

### Get Capture

**GET** `/api/captures/items/{short_uuid}/`

Retrieves a specific capture with nested images. Only returns captures owned by the authenticated user.

**Request:**
```bash
http GET :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/ -a username:password
```

**Response:** `200 OK`
```json
{
    "id": 1,
    "short_uuid": "Exh4RVhahEtkQtxhKWEngr",
    "created_at": "2025-11-26T16:08:24.710130Z",
    "voice_transcript": "Buy milk, walk the dog, call mom",
    "is_complete": false,
    "images": [
        {
            "id": 1,
            "short_uuid": "abc123xyz",
            "image": "/media/captures/2025/11/26/photo.jpg",
            "order": 0,
            "created_at": "2025-11-26T16:10:00.000000Z"
        }
    ]
}
```

**Error:** `404 Not Found` if capture doesn't exist or belongs to another user.

---

### Update Capture

**PATCH** `/api/captures/items/{short_uuid}/`

Updates capture fields (typically `voice_transcript`).

**Request:**
```bash
http PATCH :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/ \
  -a username:password \
  voice_transcript="Buy milk, walk the dog, call mom"
```

**Response:** `200 OK`
```json
{
    "id": 1,
    "short_uuid": "Exh4RVhahEtkQtxhKWEngr",
    "created_at": "2025-11-26T16:08:24.710130Z",
    "voice_transcript": "Buy milk, walk the dog, call mom",
    "is_complete": false,
    "images": []
}
```

---

### Delete Capture

**DELETE** `/api/captures/items/{short_uuid}/`

Deletes a capture and all associated images (cascading delete).

**Request:**
```bash
http DELETE :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/ -a username:password
```

**Response:** `204 No Content`

---

### List Captures

**GET** `/api/captures/items/`

Returns paginated list of captures owned by the authenticated user.

**Request:**
```bash
http GET :8000/api/captures/items/ -a username:password
```

**Response:** `200 OK`
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "short_uuid": "YaVvwusANmrRu2LnzK47hh",
            "created_at": "2025-11-26T16:35:20.711321Z",
            "voice_transcript": "Test capture",
            "is_complete": false,
            "images": []
        },
        {
            "id": 1,
            "short_uuid": "Exh4RVhahEtkQtxhKWEngr",
            "created_at": "2025-11-26T16:08:24.710130Z",
            "voice_transcript": "Buy milk",
            "is_complete": false,
            "images": []
        }
    ]
}
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

---

### Upload Images

**POST** `/api/captures/items/{short_uuid}/upload_images/`

Uploads one or more images to a capture. Maximum 20 images per capture.

**Request:**
```bash
# Upload single image
http POST :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/upload_images/ \
  -a username:password \
  --form images@photo1.jpg

# Upload multiple images
http POST :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/upload_images/ \
  -a username:password \
  --form images@photo1.jpg \
  --form images@photo2.jpg \
  --form images@photo3.jpg
```

**Response:** `201 Created`
```json
[
    {
        "id": 1,
        "short_uuid": "abc123xyz",
        "image": "/media/captures/2025/11/26/photo1.jpg",
        "order": 0,
        "created_at": "2025-11-26T16:10:00.000000Z"
    },
    {
        "id": 2,
        "short_uuid": "def456uvw",
        "image": "/media/captures/2025/11/26/photo2.jpg",
        "order": 1,
        "created_at": "2025-11-26T16:10:01.000000Z"
    }
]
```

**Error:** `400 Bad Request` if uploading would exceed 20-image limit
```json
{
    "error": "Cannot upload 5 images. Capture already has 18 images. Maximum is 20.",
    "current_count": 18,
    "max_allowed": 20
}
```

---

### Delete Image

**DELETE** `/api/captures/items/{capture_short_uuid}/images/{image_short_uuid}/`

Deletes a single image from a capture.

**Request:**
```bash
http DELETE :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/images/abc123xyz/ \
  -a username:password
```

**Response:** `204 No Content`

**Error:** `404 Not Found` if image doesn't exist or doesn't belong to the user

---

### Reorder Images

**PATCH** `/api/captures/items/{short_uuid}/reorder/`

Reorders images within a capture. Provide array of image UUIDs in desired order.

**Request:**
```bash
http PATCH :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/reorder/ \
  -a username:password \
  order:='["def456uvw", "abc123xyz", "ghi789rst"]'
```

**Response:** `200 OK`
```json
{
    "reordered": true,
    "count": 3
}
```

**Error:** `400 Bad Request` if any UUID doesn't belong to the capture
```json
{
    "error": "Image 12345678-1234-1234-1234-123456789012 does not belong to this capture"
}
```

---

### Complete Capture

**POST** `/api/captures/items/{short_uuid}/complete/`

Marks a capture as complete. This sets `is_complete=True` and can trigger downstream processing.

**Request:**
```bash
http POST :8000/api/captures/items/Exh4RVhahEtkQtxhKWEngr/complete/ \
  -a username:password
```

**Response:** `200 OK`
```json
{
    "completed": true,
    "image_count": 5
}
```

---

## Example Workflows

### Complete Capture Workflow

```bash
# 1. Create capture
CAPTURE=$(http POST :8000/api/captures/items/ -a user:pass | jq -r .short_uuid)

# 2. Upload images
http POST :8000/api/captures/items/$CAPTURE/upload_images/ \
  -a user:pass \
  --form images@photo1.jpg \
  --form images@photo2.jpg

# 3. Add transcript
http PATCH :8000/api/captures/items/$CAPTURE/ -a user:pass \
  voice_transcript="Buy groceries: milk, eggs, bread"

# 4. Mark complete
http POST :8000/api/captures/items/$CAPTURE/complete/ -a user:pass

# 5. Verify
http GET :8000/api/captures/items/$CAPTURE/ -a user:pass

# 6. Clean up
http DELETE :8000/api/captures/items/$CAPTURE/ -a user:pass
```

### Image Management Workflow

```bash
# Get capture UUID
CAPTURE="Exh4RVhahEtkQtxhKWEngr"

# Upload multiple images
http POST :8000/api/captures/items/$CAPTURE/upload_images/ \
  -a user:pass \
  --form images@img1.jpg \
  --form images@img2.jpg \
  --form images@img3.jpg

# Get image UUIDs from response
IMG1="abc123xyz"
IMG2="def456uvw"
IMG3="ghi789rst"

# Reorder: move last image to front
http PATCH :8000/api/captures/items/$CAPTURE/reorder/ \
  -a user:pass \
  order:="[\"$IMG3\", \"$IMG1\", \"$IMG2\"]"

# Delete middle image
http DELETE :8000/api/captures/items/$CAPTURE/images/$IMG1/ -a user:pass

# Verify new order
http GET :8000/api/captures/items/$CAPTURE/ -a user:pass
```

---

## Data Model

### CapturedItem
- `id` (integer, read-only): Database ID
- `short_uuid` (string, read-only): Short unique identifier (22 chars)
- `created_at` (datetime, read-only): Creation timestamp
- `voice_transcript` (string): Voice or text transcript
- `is_complete` (boolean): Completion status
- `images` (array, read-only): Nested array of CapturedImage objects

### CapturedImage
- `id` (integer, read-only): Database ID
- `short_uuid` (string, read-only): Short unique identifier
- `image` (string): URL path to image file
- `order` (integer): Display order (0-indexed)
- `created_at` (datetime, read-only): Upload timestamp

---

## Security

- All endpoints enforce ownership: users can only access their own captures
- Unauthenticated requests return `401 Unauthorized`
- Attempts to access other users' captures return `404 Not Found`
- CSRF protection enabled for session authentication
- Image uploads limited to 20 per capture
- File uploads validated as images only

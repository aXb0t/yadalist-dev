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

## Example Workflows

### Complete Capture Workflow

```bash
# 1. Create capture
CAPTURE=$(http POST :8000/api/captures/items/ -a user:pass | jq -r .short_uuid)

# 2. Add transcript
http PATCH :8000/api/captures/items/$CAPTURE/ -a user:pass \
  voice_transcript="Buy groceries: milk, eggs, bread"

# 3. Verify
http GET :8000/api/captures/items/$CAPTURE/ -a user:pass

# 4. Clean up
http DELETE :8000/api/captures/items/$CAPTURE/ -a user:pass
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

---

## Future Endpoints (Coming Soon)

- `POST /api/captures/items/{short_uuid}/images/` - Upload images
- `DELETE /api/captures/items/{short_uuid}/images/{image_uuid}/` - Delete image
- `PATCH /api/captures/items/{short_uuid}/images/reorder/` - Reorder images
- `POST /api/captures/items/{short_uuid}/complete/` - Mark capture complete

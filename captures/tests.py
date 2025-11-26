"""
Tests for the captures app.
"""
from io import BytesIO
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from captures.models import CapturedItem, CapturedImage

User = get_user_model()


def create_test_image(name='test.jpg', size=(100, 100), color='red'):
    """
    Helper function to create a test image file.
    """
    file = BytesIO()
    image = Image.new('RGB', size, color)
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')


class CaptureBaseTestCase(TestCase):
    """
    Base test case with common setup for capture tests.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.force_authenticate(user=self.user)


class CapturedItemTests(CaptureBaseTestCase):
    """
    Tests for basic CapturedItem CRUD operations.
    """
    def test_create_capture(self):
        """Test creating an empty capture."""
        response = self.client.post('/api/captures/items/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_uuid', response.data)
        self.assertIn('created_at', response.data)
        self.assertEqual(response.data['voice_transcript'], '')
        self.assertEqual(response.data['is_complete'], False)
        self.assertEqual(response.data['images'], [])

    def test_get_capture(self):
        """Test retrieving a specific capture."""
        capture = CapturedItem.objects.create(owner=self.user)
        response = self.client.get(f'/api/captures/items/{capture.short_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['short_uuid'], capture.short_uuid)

    def test_update_capture_transcript(self):
        """Test updating the voice_transcript field."""
        capture = CapturedItem.objects.create(owner=self.user)
        response = self.client.patch(
            f'/api/captures/items/{capture.short_uuid}/',
            {'voice_transcript': 'Buy milk, walk dog'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['voice_transcript'], 'Buy milk, walk dog')

    def test_delete_capture(self):
        """Test deleting a capture."""
        capture = CapturedItem.objects.create(owner=self.user)
        response = self.client.delete(f'/api/captures/items/{capture.short_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CapturedItem.objects.filter(id=capture.id).exists())

    def test_list_captures(self):
        """Test listing user's captures."""
        CapturedItem.objects.create(owner=self.user, voice_transcript='First')
        CapturedItem.objects.create(owner=self.user, voice_transcript='Second')
        response = self.client.get('/api/captures/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_ownership_isolation(self):
        """Test that users cannot access other users' captures."""
        other_capture = CapturedItem.objects.create(owner=self.other_user)
        response = self.client.get(f'/api/captures/items/{other_capture.short_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ImageUploadTests(CaptureBaseTestCase):
    """
    Tests for image upload functionality.
    """
    def test_upload_single_image(self):
        """Test uploading a single image to a capture."""
        capture = CapturedItem.objects.create(owner=self.user)
        image = create_test_image('photo.jpg')

        response = self.client.post(
            f'/api/captures/items/{capture.short_uuid}/upload_images/',
            {'images': [image]},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['order'], 0)
        self.assertIn('short_uuid', response.data[0])
        self.assertIn('image', response.data[0])

        # Verify in database
        self.assertEqual(capture.images.count(), 1)

    def test_upload_multiple_images(self):
        """Test uploading multiple images at once."""
        capture = CapturedItem.objects.create(owner=self.user)
        images = [
            create_test_image('photo1.jpg', color='red'),
            create_test_image('photo2.jpg', color='green'),
            create_test_image('photo3.jpg', color='blue'),
        ]

        response = self.client.post(
            f'/api/captures/items/{capture.short_uuid}/upload_images/',
            {'images': images},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)

        # Verify ordering
        self.assertEqual(response.data[0]['order'], 0)
        self.assertEqual(response.data[1]['order'], 1)
        self.assertEqual(response.data[2]['order'], 2)

        # Verify in database
        self.assertEqual(capture.images.count(), 3)

    def test_upload_appends_to_existing_images(self):
        """Test that new uploads append after existing images."""
        capture = CapturedItem.objects.create(owner=self.user)

        # First upload: 2 images
        images1 = [
            create_test_image('photo1.jpg'),
            create_test_image('photo2.jpg'),
        ]
        self.client.post(
            f'/api/captures/items/{capture.short_uuid}/upload_images/',
            {'images': images1},
            format='multipart'
        )

        # Second upload: 2 more images
        images2 = [
            create_test_image('photo3.jpg'),
            create_test_image('photo4.jpg'),
        ]
        response = self.client.post(
            f'/api/captures/items/{capture.short_uuid}/upload_images/',
            {'images': images2},
            format='multipart'
        )

        # New images should have order 2 and 3
        self.assertEqual(response.data[0]['order'], 2)
        self.assertEqual(response.data[1]['order'], 3)
        self.assertEqual(capture.images.count(), 4)

    def test_enforce_20_image_limit(self):
        """Test that uploads are rejected when they would exceed 20 images."""
        capture = CapturedItem.objects.create(owner=self.user)

        # Upload 18 images
        for i in range(18):
            CapturedImage.objects.create(
                owner=self.user,
                captured_item=capture,
                image=create_test_image(f'img{i}.jpg'),
                order=i
            )

        # Try to upload 3 more (would total 21)
        images = [
            create_test_image('photo19.jpg'),
            create_test_image('photo20.jpg'),
            create_test_image('photo21.jpg'),
        ]
        response = self.client.post(
            f'/api/captures/items/{capture.short_uuid}/upload_images/',
            {'images': images},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('current_count', response.data)
        self.assertEqual(response.data['current_count'], 18)
        self.assertEqual(response.data['max_allowed'], 20)

        # Verify no images were added
        self.assertEqual(capture.images.count(), 18)

    def test_upload_exactly_20_images_succeeds(self):
        """Test that uploading exactly 20 images is allowed."""
        capture = CapturedItem.objects.create(owner=self.user)
        images = [create_test_image(f'photo{i}.jpg') for i in range(20)]

        response = self.client.post(
            f'/api/captures/items/{capture.short_uuid}/upload_images/',
            {'images': images},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 20)
        self.assertEqual(capture.images.count(), 20)

    def test_upload_to_other_users_capture_fails(self):
        """Test that users cannot upload images to other users' captures."""
        other_capture = CapturedItem.objects.create(owner=self.other_user)
        image = create_test_image('photo.jpg')

        response = self.client.post(
            f'/api/captures/items/{other_capture.short_uuid}/upload_images/',
            {'images': [image]},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ImageDeleteTests(CaptureBaseTestCase):
    """
    Tests for image deletion functionality.
    """
    def test_delete_image(self):
        """Test deleting a single image."""
        capture = CapturedItem.objects.create(owner=self.user)
        image = CapturedImage.objects.create(
            owner=self.user,
            captured_item=capture,
            image=create_test_image('photo.jpg'),
            order=0
        )

        response = self.client.delete(
            f'/api/captures/items/{capture.short_uuid}/images/{image.short_uuid}/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CapturedImage.objects.filter(id=image.id).exists())

    def test_delete_image_from_other_users_capture_fails(self):
        """Test that users cannot delete images from other users' captures."""
        other_capture = CapturedItem.objects.create(owner=self.other_user)
        other_image = CapturedImage.objects.create(
            owner=self.other_user,
            captured_item=other_capture,
            image=create_test_image('photo.jpg'),
            order=0
        )

        response = self.client.delete(
            f'/api/captures/items/{other_capture.short_uuid}/images/{other_image.short_uuid}/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Verify image still exists
        self.assertTrue(CapturedImage.objects.filter(id=other_image.id).exists())

    def test_delete_nonexistent_image_fails(self):
        """Test that deleting a non-existent image returns 404."""
        capture = CapturedItem.objects.create(owner=self.user)

        response = self.client.delete(
            f'/api/captures/items/{capture.short_uuid}/images/nonexistent/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ImageReorderTests(CaptureBaseTestCase):
    """
    Tests for image reordering functionality.
    """
    def test_reorder_images(self):
        """Test reordering images within a capture."""
        capture = CapturedItem.objects.create(owner=self.user)

        # Create 3 images
        img1 = CapturedImage.objects.create(
            owner=self.user, captured_item=capture,
            image=create_test_image('img1.jpg'), order=0
        )
        img2 = CapturedImage.objects.create(
            owner=self.user, captured_item=capture,
            image=create_test_image('img2.jpg'), order=1
        )
        img3 = CapturedImage.objects.create(
            owner=self.user, captured_item=capture,
            image=create_test_image('img3.jpg'), order=2
        )

        # Reorder: 3, 1, 2
        new_order = [str(img3.uuid), str(img1.uuid), str(img2.uuid)]
        response = self.client.patch(
            f'/api/captures/items/{capture.short_uuid}/reorder/',
            {'order': new_order},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['reordered'])
        self.assertEqual(response.data['count'], 3)

        # Verify new order in database
        img1.refresh_from_db()
        img2.refresh_from_db()
        img3.refresh_from_db()

        self.assertEqual(img3.order, 0)
        self.assertEqual(img1.order, 1)
        self.assertEqual(img2.order, 2)

    def test_reorder_with_invalid_uuid_fails(self):
        """Test that reordering with an invalid UUID fails."""
        capture = CapturedItem.objects.create(owner=self.user)

        img1 = CapturedImage.objects.create(
            owner=self.user, captured_item=capture,
            image=create_test_image('img1.jpg'), order=0
        )

        # Try to reorder with a UUID that doesn't belong to this capture
        fake_uuid = '12345678-1234-1234-1234-123456789012'
        response = self.client.patch(
            f'/api/captures/items/{capture.short_uuid}/reorder/',
            {'order': [fake_uuid, str(img1.uuid)]},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_reorder_other_users_capture_fails(self):
        """Test that users cannot reorder images in other users' captures."""
        other_capture = CapturedItem.objects.create(owner=self.other_user)
        other_img = CapturedImage.objects.create(
            owner=self.other_user,
            captured_item=other_capture,
            image=create_test_image('img.jpg'),
            order=0
        )

        response = self.client.patch(
            f'/api/captures/items/{other_capture.short_uuid}/reorder/',
            {'order': [str(other_img.uuid)]},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CompleteCaptureTests(CaptureBaseTestCase):
    """
    Tests for marking captures as complete.
    """
    def test_complete_capture(self):
        """Test marking a capture as complete."""
        capture = CapturedItem.objects.create(owner=self.user)

        # Add some images
        for i in range(3):
            CapturedImage.objects.create(
                owner=self.user,
                captured_item=capture,
                image=create_test_image(f'img{i}.jpg'),
                order=i
            )

        response = self.client.post(
            f'/api/captures/items/{capture.short_uuid}/complete/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['completed'])
        self.assertEqual(response.data['image_count'], 3)

        # Verify in database
        capture.refresh_from_db()
        self.assertTrue(capture.is_complete)

    def test_complete_empty_capture(self):
        """Test marking a capture with no images as complete."""
        capture = CapturedItem.objects.create(owner=self.user)

        response = self.client.post(
            f'/api/captures/items/{capture.short_uuid}/complete/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['image_count'], 0)

    def test_complete_other_users_capture_fails(self):
        """Test that users cannot complete other users' captures."""
        other_capture = CapturedItem.objects.create(owner=self.other_user)

        response = self.client.post(
            f'/api/captures/items/{other_capture.short_uuid}/complete/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthenticationTests(TestCase):
    """
    Tests for API authentication requirements.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_unauthenticated_access_fails(self):
        """Test that unauthenticated requests are rejected."""
        response = self.client.get('/api/captures/items/')
        # DRF returns 403 Forbidden for unauthenticated requests by default
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_authenticated_access_succeeds(self):
        """Test that authenticated requests succeed."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/captures/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from zivotopis.models import Post, Image
from django.contrib.auth.models import User
import json

class ImageAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(title="Test Post", text="Obsah test postu", author=self.user)
        self.image = Image.objects.create(post=self.post, image="post_images/test.jpg")
        self.url = reverse('image-list')  # DRF router name

    def test_get_images_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertIn('image', data[0])

        # relatívna cesta
        actual_path = data[0]['image'].replace('http://testserver', '')
        self.assertEqual(actual_path, '/media/post_images/test.jpg')


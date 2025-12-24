from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from zivotopis.models import Post, Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from io import BytesIO
from PIL import Image as PilImage

def get_test_image_file():
    file = BytesIO()
    image = PilImage.new("RGB", (10, 10), color="red")
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile("test.jpg", file.read(), content_type="image/jpeg")


class ImageAPITest(APITestCase):
    def setUp(self): 
        self.user = User.objects.create_user(username="testuser", password="12345") 
        self.post = Post.objects.create(title="Test Post", text="Obsah test postu", author=self.user) 
        self.image = Image.objects.create(post=self.post, image="post_images/test.jpg") 
        self.url_list = reverse('images-list') # /api/images/ 
        self.url_detail = reverse('images-detail', args=[self.image.pk]) # /api/images/<id>/

    def test_get_images_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertIn('image', data[0])

        # relatívna cesta
        actual_path = data[0]['image'].replace('http://testserver', '')
        self.assertEqual(actual_path, '/media/post_images/test.jpg')

    def test_create_image_authenticated(self): 
        # 🦆 Kačička, najprv sa prihlásim 
        self.client.login(username="testuser", password="12345") 
        # 🦆 Pripravím falošný obrázok ako súbor 
        image_file = get_test_image_file() 
        data = {"post": self.post.pk, "image": image_file}
        # 🦆 Pošlem POST request na API 
        response = self.client.post(self.url_list, data, format="multipart") 
        # 🦆 Očakávam, že sa obrázok uloží 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        self.assertTrue(Image.objects.filter(post=self.post).exists()) 
        
    def test_create_image_unauthenticated(self): 
        # 🦆 Kačička, teraz to skúsi neprihlásený používateľ 
        image_file = get_test_image_file() 
        data = {"post": self.post.pk, "image": image_file}
        response = self.client.post(self.url_list, data, format="multipart") 
        # 🦆 Očakávam, že ho to nepustí a redirectne na login 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_image_authenticated(self): 
        # 🦆 Kačička, prihlásim sa 
        self.client.login(username="testuser", password="12345") 
        # 🦆 Pošlem DELETE request na detailnú URL obrázka 
        response = self.client.delete(self.url_detail) 
        # 🦆 Očakávam, že odpoveď bude 204 NO CONTENT 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 
        # 🦆 A že obrázok už neexistuje v databáze 
        self.assertFalse(Image.objects.filter(id=self.image.pk).exists()) 

    def test_delete_image_unauthenticated(self): 
        # 🦆 Kačička, neprihlásený používateľ skúsi zmazať obrázok 
        response = self.client.delete(self.url_detail) 
        # 🦆 Očakávam, že ho to nepustí → 403 FORBIDDEN 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
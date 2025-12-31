from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from zivotopis.models import Post

class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_post_authenticated(self):
        self.client.login(username="testuser", password="12345")
        data = {"title": "Nový post", "text": "Obsah", "category": "bio"}
        response = self.client.post(reverse('post_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Nový post").exists())

    def test_create_post_unauthenticated(self):
        # Varianty dát môžu byť rôzne, hlavne testuješ redirect
        data1 = {"title": "Nový post", "text": "Obsah"}
        data2 = {"title": "Nový post", "text": "Obsah", "category": "Práca"}

        # Test 1: bez category
        response1 = self.client.post(reverse('post_new'), data1)
        self.assertEqual(response1.status_code, 302)  # redirect na login

        # Test 2: s category
        response2 = self.client.post(reverse('post_new'), data2)
        self.assertEqual(response2.status_code, 302)  # redirect na login

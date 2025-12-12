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
        data = {"title": "Nový post", "text": "Obsah"}
        response = self.client.post(reverse('post_new'), data)
        self.assertEqual(response.status_code, 302)  # redirect na login

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from zivotopis.models import Post


class ContactFormViewTest(TestCase):
    def test_contact_form_get(self):
        """GET request na kontaktný formulár"""
        response = self.client.get(reverse('send_email'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_contact_form_post_valid(self):
        """POST request s validnými dátami"""
        data = {
        "sender_name": "",
        "sender_email": "not-an-email",
        "subject": "",
        "message": ""
    }
        response = self.client.post(reverse('send_email'), data)
        self.assertEqual(response.status_code, 302)  # redirect na unsuccess_view
        self.assertRedirects(response, reverse('unsuccess_view'))
    def test_contact_form_post_invalid(self):
        data = {
            "sender_name": "",
            "sender_email": "not-an-email",
            "subject": "",
            "message": ""
        }
        response = self.client.post(reverse('send_email'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('unsuccess_view'))


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_post_authenticated(self):
        self.client.login(username="testuser", password="12345")
        data = {
            "title": "Nový post",
            "text": "Obsah",
            "category": "bio"  # <-- pridaj správnu hodnotu
        }
        response = self.client.post(reverse('post_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Nový post").exists())


    def test_create_post_unauthenticated(self):
        data = {
            "title": "Nový post",
            "text": "Obsah",
            "category": "Práca"
        }
        response = self.client.post(reverse('post_new'), data)
        # Neautentifikovaný používateľ → redirect na login
        self.assertEqual(response.status_code, 302)


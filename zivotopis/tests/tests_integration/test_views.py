from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from zivotopis.models import Post, Image


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    # --- POST NEW ---
    def test_create_post_authenticated(self):
        self.client.login(username="testuser", password="12345")
        data = {"title": "Nový post", "text": "Obsah", "category": "bio"}
        response = self.client.post(reverse('post_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Nový post").exists())

    def test_create_post_unauthenticated(self):
        data = {"title": "Nový post", "text": "Obsah"}
        response = self.client.post(reverse('post_new'), data)
        self.assertEqual(response.status_code, 302)

    def test_get_create_post_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "zivotopis/post_edit.html")

    def test_get_create_post_unauthenticated(self):
        response = self.client.get(reverse('post_new'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('post_new')}"
        )

    # --- LIST & DETAIL ---
    def test_post_list(self):
        Post.objects.create(author=self.user, title="A", text="B", published_date=timezone.now())
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "zivotopis/post_list.html")

    def test_post_detail(self):
        post = Post.objects.create(author=self.user, title="A", text="B")
        response = self.client.get(reverse("post_detail", args=[post.pk]))
        self.assertEqual(response.status_code, 200)

    # --- EDIT ---
    def test_get_post_edit_authenticated(self):
        post = Post.objects.create(author=self.user, title="A", text="B")
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("post_edit", args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "zivotopis/post_edit.html")

    def test_post_edit_valid(self):
        post = Post.objects.create(author=self.user, title="A", text="B")
        self.client.login(username="testuser", password="12345")
        data = {"title": "Updated", "text": "New text", "category": "bio"}
        response = self.client.post(reverse("post_edit", args=[post.pk]), data)
        self.assertEqual(response.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated")

    def test_post_edit_invalid(self):
        post = Post.objects.create(author=self.user, title="A", text="B")
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("post_edit", args=[post.pk]), {"title": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    # --- PUBLISH & REMOVE ---
    def test_post_publish(self):
        post = Post.objects.create(author=self.user, title="A", text="B")
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("post_publish", args=[post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_post_remove(self):
        post = Post.objects.create(author=self.user, title="A", text="B")
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("post_remove", args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    # --- IMAGE DELETE ---
    def test_image_delete(self):
        post = Post.objects.create(author=self.user, title="A", text="B")
        image = Image.objects.create(post=post, image="test.jpg")
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("image_delete", args=[image.pk]))
        self.assertEqual(response.status_code, 302)

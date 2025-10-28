from django.test import TestCase
from django.contrib.auth.models import User
from zivotopis.models import Post


class PostModelTest(TestCase):
    def setUp(self):
        # 1️⃣ Vytvoríme testovacieho používateľa
        self.user = User.objects.create_user(username="testuser", password="12345")

        # 2️⃣ Vytvoríme testovací Post s autorom
        self.post = Post.objects.create(
            title="Test Post",
            text="Obsah testovacieho príspevku",
            author=self.user
        )

        # 3️⃣ Publikujeme post, aby sa zobrazoval v post_list view
        self.post.publish()

    def test_post_str(self):
        """Test, či __str__ metóda vracia názov postu"""
        self.assertEqual(str(self.post), "Test Post")

    def test_post_list_view(self):
        """Test, či domovská stránka obsahuje náš post"""
        response = self.client.get("/")  # URL tvojej list view
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_creation(self):
        """Test, či sa Post správne ukladá a má autora"""
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.text, "Obsah testovacieho príspevku")



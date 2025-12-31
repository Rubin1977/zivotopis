from django.test import SimpleTestCase
from django.urls import reverse, resolve
from zivotopis import views
from zivotopis.views import CenyDeleteView, PostViewSet

class TestUrls(SimpleTestCase):
    def test_send_email_url(self):
        url = reverse('send_email')
        self.assertEqual(resolve(url).func.__name__, views.send_email.__name__)

    def test_delete_url(self): 
        url = reverse('delete', args=[1]) # v urls.py máš path('reality/delete/<int:pk>/', ...) 
        resolved = resolve(url) 
        self.assertEqual(resolved.func.view_class.__name__, CenyDeleteView.__name__)

    def test_post_detail_url(self): 
        # V urls.py máš router.register(r'posts', PostViewSet) 
        # # To ti vytvorí routu posts-detail → /api/posts/<pk>/ 
        url = reverse('posts-detail', args=[1]) #pk=1 
        resolved = resolve(url) 
        self.assertEqual(resolved.func.cls, PostViewSet)


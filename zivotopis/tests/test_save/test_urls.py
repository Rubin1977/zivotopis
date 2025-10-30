from django.test import SimpleTestCase
from django.urls import reverse, resolve
from zivotopis import views

class TestUrls(SimpleTestCase):
    def test_send_email_url(self):
        url = reverse('send_email')
        self.assertEqual(resolve(url).func.__name__, views.send_email.__name__)

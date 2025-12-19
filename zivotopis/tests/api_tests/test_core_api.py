from django.test import TestCase
from django.urls import reverse
import json

class CoreAPITest(TestCase):
    def setUp(self):
        # Base endpoints podľa tvojho deployed API
        self.endpoints = {
            "posts": "/api/posts/",
            "images": "/api/images/",
            "emails": "/api/emails/",
            "gallery": "/api/gallery/",
            "ceny": "/api/ceny/"
        }

    def test_endpoints_available(self):
        """Test, že všetky endpointy sú dostupné (HTTP 200 alebo správny kód)"""
        for name, url in self.endpoints.items():
            response = self.client.get(url)
            if name == "emails":
                # GET na /emails/ nie je povolený → očakávame 405
                self.assertEqual(response.status_code, 405, f"{name} endpoint mal vrátiť 405")
            else:
                self.assertEqual(response.status_code, 200, f"{name} endpoint nedostupný")

    def test_json_structure(self):
        """Skontrolujeme základnú štruktúru JSON odpovede"""
        # testujeme len posts a images ako príklad
        for name in ["posts", "images"]:
            url = self.endpoints[name]
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.content)
            self.assertIsInstance(data, list, f"{name} odpoveď nie je list")
            
            if data:
                item = data[0]
                if name == "posts":
                    for key in ["id", "title", "text", "author"]:
                        self.assertIn(key, item, f"{key} chýba v {name}")
                elif name == "images":
                    for key in ["id", "image", "post"]:
                        self.assertIn(key, item, f"{key} chýba v {name}")

    def test_no_sensitive_data(self):
        """Overíme, že v odpovediach nie sú citlivé údaje"""
        url = self.endpoints["posts"]
        response = self.client.get(url)
        self.assertNotIn("password", response.content.decode(), "API obsahuje citlivé údaje")

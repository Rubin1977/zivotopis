from django.test import TestCase
from zivotopis.forms import EmailForm

class ContactFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "sender_name": "Rastislav",
            "sender_email": "rastislav@example.com",
            "subject": "Test",
            "message": "Ahoj, toto je test."
        }
        form = EmailForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "sender_name": "",
            "sender_email": "not-an-email",
            "subject": "",
            "message": ""
        }
        form = EmailForm(data=data)
        self.assertFalse(form.is_valid())
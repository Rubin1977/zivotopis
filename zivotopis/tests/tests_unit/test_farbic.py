from django.test import SimpleTestCase
from zivotopis.templatetags.farbic import farbic_class

class TestFarbicClass(SimpleTestCase):

    def test_non_numeric_returns_secondary(self):
        self.assertEqual(farbic_class("abc"), "text-secondary")
        self.assertEqual(farbic_class(None), "text-secondary")
        self.assertEqual(farbic_class(""), "text-secondary")

    def test_positive_number(self):
        self.assertEqual(farbic_class(5), "text-success")
        self.assertEqual(farbic_class("10"), "text-success")

    def test_negative_number(self):
        self.assertEqual(farbic_class(-3), "text-danger")
        self.assertEqual(farbic_class("-7"), "text-danger")

    def test_zero(self):
        self.assertEqual(farbic_class(0), "text-secondary")
        self.assertEqual(farbic_class("0"), "text-secondary")

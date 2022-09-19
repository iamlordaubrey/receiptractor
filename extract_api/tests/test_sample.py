from django.test import TestCase
from rest_framework.test import APITestCase


class SampleTest(APITestCase):
    def test_summation(self):
        self.assertTrue(1, 1)
        self.assertEqual(1+1, 2)

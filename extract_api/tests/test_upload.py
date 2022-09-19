import os

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

MODULE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(MODULE_DIR, 'test_files/receipt_sample.txt')


class ReceiptUploadTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='john',
            email='john1234@gmail.com',
            password='john1234',
        )
        refresh = RefreshToken.for_user(self.test_user)

        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_endpoint(self):
        receipt_file = open(FILE_PATH, 'r')
        response = self.api_client.post(reverse('receipts'), {'receipt': receipt_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()
        self.assertIn('blocks', response_json)
        self.assertEqual(len(response_json['blocks']), 8)

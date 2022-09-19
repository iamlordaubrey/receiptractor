import os

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from extract_api.models import Receipt

MODULE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(MODULE_DIR, 'test_files/receipt_sample.txt')


class ReceiptModelTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='john',
            email='john1234@gmail.com',
            password='john1234',
        )
        refresh = RefreshToken.for_user(self.test_user)

        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.receipt_file = open(FILE_PATH, 'r')
        self.api_client.post(reverse('receipts'), {'receipt': self.receipt_file})

    def test_receipt_labels(self):
        receipt = Receipt.objects.all().first()
        self.assertEqual(receipt.file_name, 'receipt_sample.txt')
        self.assertIn('Bill no.3-7721', receipt.bill_info)

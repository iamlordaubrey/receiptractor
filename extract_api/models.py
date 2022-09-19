import uuid

from django.db import models


class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file_name = models.CharField(max_length=100)
    company_info = models.CharField(max_length=500)
    bill_info = models.CharField(max_length=500)
    customer_order = models.CharField(max_length=500)
    total = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

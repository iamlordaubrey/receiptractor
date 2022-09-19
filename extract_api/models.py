from django.db import models


class Receipt(models.Model):
    id = models.UUIDField(primary_key=True)
    file_name = models.CharField(max_length=100)
    company_info = models.CharField(max_length=250)
    body = models.FileField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from .models import Receipt


class FileSerializer(serializers.ModelSerializer):
    receipt = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['txt', ])])

    class Meta:
        model = Receipt
        fields = ('receipt',)

from rest_framework import serializers
from .models import Receipt


class FileSerializer(serializers.ModelSerializer):
    receipt = serializers.FileField()

    class Meta:
        model = Receipt
        fields = ('receipt',)

    # class Meta:
    #     model = Receipt
    #     fields = ('id', 'file_name')

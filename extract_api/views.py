from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from extract_api.models import Receipt
from extract_api.serializers import FileSerializer
from extract_api.utils import text_blocks_extractor


class ReceiptAPI(APIView):
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            receipt_file = request.FILES['receipt']
            text_extract, blocks = text_blocks_extractor(receipt_file)

            receipt_object = Receipt(
                file_name=receipt_file.name,
                company_info=text_extract[0],
                bill_info=text_extract[1],
                customer_order=text_extract[2],
                total=text_extract[3],
            )
            receipt_object.save()

            return Response({'blocks': blocks}, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

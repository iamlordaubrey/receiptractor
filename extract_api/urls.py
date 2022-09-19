from django.urls import path
from extract_api import views

urlpatterns = [
    path('receipts', views.ReceiptAPI.as_view()),
]

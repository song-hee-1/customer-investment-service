from django.urls import path

from .views import TransferVerifyAPI, TransferAPI

urlpatterns = [
    path('transfers-verifications/', TransferVerifyAPI.as_view(), name='transfer-verification'),
    path('transfers/', TransferAPI.as_view(), name='transfer'),
]

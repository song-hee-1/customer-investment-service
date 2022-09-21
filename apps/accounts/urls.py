from django.urls import path

from .views import GetHoldingInvestListAPI, GetDetailInvestAPI, GetInvestAPI, TransferVerifyAPI, TransferAPI

urlpatterns = [
    path('investments/holdings', GetHoldingInvestListAPI.as_view()),
    path('investments/detail', GetDetailInvestAPI.as_view()),
    path('investments/', GetInvestAPI.as_view()),
    path('transfer-verify/', TransferVerifyAPI.as_view()),
    path('transfer/', TransferAPI.as_view()),
]

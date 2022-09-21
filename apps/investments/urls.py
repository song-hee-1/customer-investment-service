from django.urls import path

from apps.investments.views import GetHoldingInvestListAPI, GetInvestAPI

urlpatterns = [
    path('investments/holdings', GetHoldingInvestListAPI.as_view(), name='investments-holdings'),
    path('investments/', GetInvestAPI.as_view(), name='investments'),
]

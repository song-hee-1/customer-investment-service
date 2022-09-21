from django.urls import path

from apps.accounts.views import GetHoldingInvestListAPI, GetInvestAPI

urlpatterns = [
    path('investments/holdings', GetHoldingInvestListAPI.as_view()),
    path('investments/', GetInvestAPI.as_view()),
]

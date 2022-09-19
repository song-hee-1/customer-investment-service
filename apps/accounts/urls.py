from django.urls import path

from .views import GetHoldingInvestListAPI, GetDetailInvestAPI, GetInvestAPI

urlpatterns = [
    path('investments/holdings', GetHoldingInvestListAPI.as_view()),
    path('investments/detail', GetDetailInvestAPI.as_view()),
    path('investments/', GetInvestAPI.as_view()),
]

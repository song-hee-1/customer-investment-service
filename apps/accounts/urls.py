from django.urls import path

from .views import GetHoldingInvestListAPI, GetDetailInvestAPI
urlpatterns = [
    path('investments/holdings', GetHoldingInvestListAPI.as_view()),
    path('investments/', GetDetailInvestAPI.as_view()),
]

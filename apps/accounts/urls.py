from django.urls import path

from .views import GetHoldingInvestListAPI

urlpatterns = [
    path('investments/', GetHoldingInvestListAPI.as_view()),
]

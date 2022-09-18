from rest_framework import generics

from apps.investments.models import Investment
from . serializers import StockHoldingSerializer


class GetHoldingInvestListAPI(generics.ListAPIView):
    serializer_class = StockHoldingSerializer

    def get_queryset(self):
        return Investment.objects.all()

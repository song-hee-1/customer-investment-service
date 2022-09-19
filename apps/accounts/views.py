from rest_framework import generics

from apps.accounts.models import Account
from apps.investments.models import Investment

from . serializers import StockHoldingSerializer, InvestDetailSerializer


class GetHoldingInvestListAPI(generics.ListAPIView):
    serializer_class = StockHoldingSerializer

    def get_queryset(self):
        return Investment.objects.all()


class GetDetailInvestAPI(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestDetailSerializer

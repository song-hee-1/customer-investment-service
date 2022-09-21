from rest_framework import generics

from apps.accounts.models import Account
from apps.investments.models import Investment

from apps.accounts.serializers import StockHoldingSerializer, InvestDetailSerializer, InvestSerializer


class GetHoldingInvestListAPI(generics.ListAPIView):
    serializer_class = StockHoldingSerializer

    def get_queryset(self):
        return Investment.objects.all()


class GetDetailInvestAPI(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestDetailSerializer


class GetInvestAPI(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestSerializer



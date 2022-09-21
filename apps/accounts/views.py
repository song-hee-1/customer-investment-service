from rest_framework import generics

from apps.accounts.models import Account
from apps.investments.models import Investment

from apps.accounts.serializers import StockHoldingSerializer, InvestDetailSerializer, InvestSerializer


# 보유 종목 화면 API
class GetHoldingInvestListAPI(generics.ListAPIView):
    serializer_class = StockHoldingSerializer

    def get_queryset(self):
        return Investment.objects.all()


# 투자 화면 API
class GetInvestAPI(generics.ListAPIView):
    queryset = Account.objects.all()

    def get_serializer_class(self):

        is_simple = self.request.GET.get('is_simple', None)

        if is_simple:
            return InvestSerializer
        else:
            return InvestDetailSerializer

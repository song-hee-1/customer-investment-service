from rest_framework import generics

from apps.accounts.models import Account
from apps.investments.models import Investment

from apps.investments.serializers import StockHoldingSerializer, InvestDetailSerializer, InvestSerializer


# 보유 종목 화면 API
class GetHoldingInvestListAPI(generics.ListAPIView):

    def get_queryset(self):
        user = self.request.user
        queryset = Investment.objects.filter(account_id__user_id=user.id)
        return queryset

    serializer_class = StockHoldingSerializer


# 투자 화면 API
class GetInvestAPI(generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        queryset = Account.objects.filter(user_id=user.id)
        return queryset

    def get_serializer_class(self):

        is_simple = self.request.GET.get('is_simple', None)

        if is_simple:
            return InvestSerializer
        else:
            return InvestDetailSerializer

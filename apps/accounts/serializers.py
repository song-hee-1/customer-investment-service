from rest_framework import serializers

from django.db.models import Sum, F

from apps.investments.models import Investment
from apps.accounts.models import Account


# 보유종목 화면 serializer
class StockHoldingSerializer(serializers.ModelSerializer):
    # 보유 종목의 평가 금액
    market_value = serializers.SerializerMethodField(method_name='get_market_value')

    def get_market_value(self, obj):
        return obj.market_value

    class Meta:
        model = Investment
        depth = 2
        exclude = ['id', 'investment_principal', 'quantity', 'investment_time', 'account']


# 투자상세 화면을 위한 Account 세부 serializer
class AccountSerializer(serializers.ModelSerializer):
    stock_securities = serializers.ReadOnlyField(source='stock_securities.name')

    class Meta:
        model = Account
        fields = ['id', 'account_name', 'account_number', 'account_total_investment_principal', 'stock_securities']


# 투자상세 화면 serializer
class InvestDetailSerializer(serializers.ModelSerializer):
    account_total_asset = serializers.SerializerMethodField(method_name='get_account_total_asset')
    total_profit = serializers.SerializerMethodField()
    rate_of_return = serializers.SerializerMethodField(method_name='get_rate_of_return')

    # 고민 : total_asset 계산식이 여러번 사용되는데, 상속하는 등 다시 이용할 수 없는 방법은 없는 것인가?
    def get_account_total_asset(self, obj):
        total_asset = Account.objects.filter(id=obj.id).values('id').annotate(
            account_total_asset= Sum(
                F('investment_account_number__quantity') *
                F('investment_account_number__investment_stock__current_price')
            ))[0]['account_total_asset']
        return total_asset

    def get_total_profit(self, obj):
        total_asset = Account.objects.filter(id=obj.id).values('id').annotate(
            account_total_asset=Sum(
                F('investment_account_number__quantity') *
                F('investment_account_number__investment_stock__current_price')
            ))[0]['account_total_asset']
        return total_asset - obj.account_total_investment_principal

    def get_rate_of_return(self, obj):
        total_asset = Account.objects.filter(id=obj.id).values('id').annotate(
            account_total_asset=Sum(
                F('investment_account_number__quantity') *
                F('investment_account_number__investment_stock__current_price')
            ))[0]['account_total_asset']
        total_profit = total_asset - obj.account_total_investment_principal
        return round((total_profit / obj.account_total_investment_principal) * 100, 2)

    class Meta:
        model = Account
        depth = 1
        exclude = ['user', 'create_time', 'investment']

from rest_framework import serializers

from django.db.models import Sum, F

from apps.investments.models import Investment
from apps.accounts.models import Account, Transfer


# 보유종목 화면 serializer
class StockHoldingSerializer(serializers.ModelSerializer):
    # 보유 종목의 평가 금액
    market_value = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        depth = 2
        exclude = ['id', 'investment_principal', 'quantity', 'investment_time', 'account']

    def get_market_value(self, obj):
        return obj.market_value


# 투자상세 화면을 위한 Account 세부 serializer
class AccountSerializer(serializers.ModelSerializer):
    stock_securities = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ['id', 'account_name', 'account_number', 'account_total_investment_principal', 'stock_securities']


# 투자상세 화면 serializer
class InvestDetailSerializer(serializers.ModelSerializer):
    # 계좌 총 자산
    account_total_asset = serializers.SerializerMethodField()
    # 총 수익금
    total_profit = serializers.SerializerMethodField()
    # 수익률
    rate_of_return = serializers.SerializerMethodField()

    class Meta:
        model = Account
        depth = 1
        exclude = ['user', 'create_time', 'investment']

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


# 투자 화면 serializer
class InvestSerializer(serializers.ModelSerializer):
    # 계좌 총 자산
    account_total_asset = serializers.SerializerMethodField(method_name='get_account_total_asset')

    class Meta:
        model = Account
        depth = 1
        exclude = ['user', 'create_time', 'investment', 'account_total_investment_principal']

    def get_account_total_asset(self, obj):
        total_asset = Account.objects.filter(id=obj.id).values('id').annotate(
            account_total_asset= Sum(
                F('investment_account_number__quantity') *
                F('investment_account_number__investment_stock__current_price')
            ))[0]['account_total_asset']
        return total_asset


class TransferInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'


class TransferOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['transfer_identifier']

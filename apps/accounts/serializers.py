from rest_framework import serializers

from apps.investments.models import Investment


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

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.investments.models import Investment
from apps.accounts.models import User, Account, StockSecurities
from apps.stocks.models import Stock, AssetGroup


class InvestmentViewTestCase(APITestCase):
    """ Investment view인 투자 화면, 투자 상세화면, 보유종목 화면이 정상 작동(GET)하는지 확인하기 위한 테스트 """

    def setUp(self):
        User.objects.create_user(
            username='핑핑이언니', password='0000', email="test@test.com", phone_number='010-1234-5678'
        )
        self.client.login(email='test@test.com', password='0000')
        StockSecurities.objects.create(
            name="핑핑증권사"
        )
        Account.objects.create(
            account_number=123123, account_name="핑핑이의 간식길을 위하여", stock_securities_id=1, user_id=1,
            account_total_investment_principal="1000000"
        )
        AssetGroup.objects.create(
            name="강아지채권"
        )
        stock_instance = Stock.objects.create(
            isin="pingping", stock_name="핑핑주식", current_price="2000000", asset_group_id="1"
        )
        Investment.objects.create(
            quantity=1, account_id=1, investment_stock=stock_instance, investment_principal=1000000
        )

    def test_investment_datail_view(self):
        response = self.client.get(reverse('investments'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_investment_simple_view(self):
        response = self.client.get(reverse('investments'), kwargs={'is_simple': True})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_investment_holding_view(self):
        response = self.client.get(reverse('investments-holdings'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

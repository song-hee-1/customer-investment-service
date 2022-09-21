from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.investments.models import Investment
from apps.accounts.models import User, Account, StockSecurities
from apps.stocks.models import Stock, AssetGroup
from apps.transfers.models import Transfer


class TransferViewTestCase(APITestCase):
    """ Transfer view가 정상 작동하는지 확인하기 위한 테스트 """

    def setUp(self):
        User.objects.create_user(
            username='핑핑이언니', password='0000', email="test@test.com", phone_number='010-1234-5678'
        )
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
        Transfer.objects.create(account_number=123123, user_name="핑핑이언니", transfer_amount=1000000,
            signature="$2b$12$i2OPTqk9NC8YrUnuBb4RpepwLKdx8kzhqxxvtsWv0c3ESxik2oLju"
        )
        self.client.login(email='test@test.com', password='0000')

    def test_phase1_fail_not_exists_user(self):
        data = {
            'account_number': 123123,
            'user_name': '존재하지 않는 이름',
            'transfer_amount': '1000000'
        }
        response = self.client.post(reverse('transfer-verification'), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phase1_fail_not_exists_account(self):
        data = {
            'account_number': 9999999,
            'user_name': '핑핑이언니',
            'transfer_amount': '1000000'
        }
        response = self.client.post(reverse('transfer-verification'), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phase1_success(self):
        data = {
            'account_number': 123123,
            'user_name': '핑핑이언니',
            'transfer_amount': '1000000'
        }
        response = self.client.post(reverse('transfer-verification'), data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_phase2_fail_wrong_signature(self):
        wrong_signature = "$2b$12$i2OPTqk9NCv0c3ESxik2oL8YrUnuBb4RpepwLKdx8kzhqxxvtsWju"
        response = self.client.post(reverse('transfer'), {"signature": wrong_signature})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


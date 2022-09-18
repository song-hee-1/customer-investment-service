from django.db import models


class Investment(models.Model):
    # 증권 계좌를 삭제한다는 것은 더이상 투자를 하지 않는다는 것으로 판단하여 같이 삭제되도록 설정
    account_number = models.ForeignKey("accounts.Account", on_delete=models.CASCADE,
                                       related_name="investment_account_number")
    # 증권이 사라진다고 해도 투자내역은 남아있어야 하기 때문에 참조 무결성을 해치더라도 깂을 그대로 저장하도록 설정
    investment_stock = models.ForeignKey("stocks.Stock", on_delete=models.DO_NOTHING, db_column='investment_stock_isin',
                                         related_name="user_investment_stock")
    investment_principal = models.PositiveIntegerField(verbose_name="투자 원금")
    quantity = models.PositiveIntegerField(verbose_name="투자 수량")
    investment_time = models.DateTimeField(auto_now_add=True, verbose_name="투자한 날짜")

    class Meta:
        verbose_name = "투자"
        verbose_name_plural = "투자 목록"
        db_table = "investment"

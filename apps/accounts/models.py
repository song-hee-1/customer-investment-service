from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# 사용자 모델
class User(AbstractUser):
    # 동명이인이 있어 username의 unique를 False로 하고, email 값으로 로그인하도록 변경
    username = models.CharField(max_length=40, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=13, unique=True,
                                    help_text="휴대폰 번호는 다음과 같은 형식으로 입력해주세요 : 010-1234-5678")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        db_table = "user"

    def __str__(self):
        return self.username


# 계좌 모델
class Account(models.Model):
    # 유저가 삭제 된다는 것은 회원 탈퇴를 의미하므로 유저 삭제시 계좌의 유저 정보도 같이 삭제되도록 설정
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    account_number = models.IntegerField(verbose_name="계좌번호")
    account_name = models.CharField(max_length=10, verbose_name="계좌명")
    # 고객이 계좌에서 증권 회사를 확인할 수 있도록 증권 회사 삭제 불가능하도록 설정
    stock_securities = models.ForeignKey("StockSecurities", related_name="account_stock_securities",
                                         on_delete=models.PROTECT)
    account_total_asset = models.PositiveIntegerField(verbose_name="계좌 총 자산")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="계좌 생성 날짜")
    investment = models.ManyToManyField(
        'stocks.Stock',
        through="investments.Investment",
        related_name="investment_account",
        blank=True,
        verbose_name="투자내역"
    )

    class Meta:
        verbose_name = "계좌"
        verbose_name_plural = "계좌 목록"
        db_table = "account"

    def __str__(self):
        return self.account_name


# 증권사 모델
class StockSecurities(models.Model):
    name = models.CharField(max_length=20, verbose_name="증권사")

    class Meta:
        verbose_name = "증권사"
        verbose_name_plural = "증권사 목록"
        db_table = "stock_securities"

    def __str__(self):
        return self.name

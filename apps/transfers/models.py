from django.db import models

# 입금 모델
class Transfer(models.Model):
    transfer_identifier = models.BigAutoField(primary_key=True)
    account_number = models.IntegerField()
    user_name = models.CharField(max_length=40)
    transfer_amount = models.PositiveIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "투자금 입금"
        verbose_name_plural = "투자금 입금 목록"
        db_table = "transfer"

    def __str__(self):
        return str(self.transfer_identifier)

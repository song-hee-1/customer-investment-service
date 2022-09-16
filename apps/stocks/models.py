from django.db import models


# 증권 모델
class Stock(models.Model):
    isin = models.CharField(max_length=12, primary_key=True, verbose_name="ISIN")
    stock_name = models.CharField(max_length=20, verbose_name="종목명")
    current_price = models.PositiveIntegerField(verbose_name="현재가")
    # 증권 자산그룹의 성격을 고려했을 때 삭제될 일이 적고, 각 증권이 자산그룹을 참조해야하므로 삭제가 불가능하도록 설정
    asset_group = models.ForeignKey("AssetGroup", related_name="stock_asset_group", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "증권"
        verbose_name_plural = "증권 목록"
        db_table = "stock"

    def __str__(self):
        return self.stock_name


# 증권 자산그룹 모델
class AssetGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name="자산군")

    class Meta:
        verbose_name = "증권 자산그룹"
        verbose_name_plural = "증권 자산그룹 목록"
        db_table = "asset_group"

    def __str__(self):
        return self.name

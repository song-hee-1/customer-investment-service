import os
from datetime import datetime
from pathlib import Path

from .models import AssetGroup, Stock

import pandas as pd

from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent


@transaction.atomic()
def crontab_stock_app_job():

    asset_group_data = os.path.join(BASE_DIR, 'stocks/data/asset_group_table.xlsx')
    asset_group_info_set = pd.read_excel(asset_group_data)

    for i, row in asset_group_info_set.iterrows():
        AssetGroup.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
            }
        )

    print(f"{datetime.now()} : Successfully update asset group table")

    stock_data = os.path.join(BASE_DIR, 'stocks/data/stock_table.xlsx')
    stock_info_set = pd.read_excel(stock_data)

    for i, row in stock_info_set.iterrows():
        Stock.objects.update_or_create(
            isin=row['isin'],
            defaults={
                'stock_name': row['stock_name'],
                'current_price': row['current_price'],
                'asset_group_id': row['asset_group_id'],
            }
        )

    print(f"{datetime.now()} : Successfully update stock table")

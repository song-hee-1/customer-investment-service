import os
from datetime import datetime
from pathlib import Path

from apps.stocks.models import Stock
from .models import Investment

import pandas as pd

from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent

@transaction.atomic()
def crontab_investment_app_job():
    investment_data = os.path.join(BASE_DIR, 'investments/data/investment_table.xlsx')
    investment_info_set = pd.read_excel(investment_data)

    for i, row in investment_info_set.iterrows():
        stock_instance = Stock.objects.get(isin=row['investment_stock_isin'])
        Investment.objects.update_or_create(
            id=row['id'],
            defaults={
                'account_id': row['account_id'],
                'investment_stock': stock_instance,
                'investment_principal': row['investment_principal'],
                'quantity': row['quantity'],
                'investment_time': row['investment_time'],
            }
        )

    print(f"{datetime.now()} : Successfully update investment table")

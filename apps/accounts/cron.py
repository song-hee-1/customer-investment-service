import os
from datetime import datetime
from pathlib import Path

from .models import User, Account, StockSecurities

import pandas as pd

from django.contrib.auth.hashers import make_password
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent


@transaction.atomic()
def crontab_accounts_app_job():
    user_file = os.path.join(BASE_DIR, 'accounts/data/user_table.xlsx')
    user_info_set = pd.read_excel(user_file)

    stock_securities_file = os.path.join(BASE_DIR, 'accounts/data/stock_securities_table.xlsx')
    stock_securities_info_set = pd.read_excel(stock_securities_file)

    account_file = os.path.join(BASE_DIR, 'accounts/data/account_table.xlsx')
    account_info_set = pd.read_excel(account_file)


    for i, row in user_info_set.iterrows():
        User.objects.update_or_create(
            id=row['id'],
            defaults={
                'username': row['username'],
                'password': make_password('0000'),
                'is_superuser': row['is_superuser'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'phone_number': row['phone_number'],
                'is_staff': row['is_staff'],
                'is_active': row['is_active'],
                'date_joined': row['date_joined'],
            }
        )

    print(f"{datetime.now()} : Successfully update user table")


    for i, row in stock_securities_info_set.iterrows():
        StockSecurities.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
            }
        )

    print(f"{datetime.now()} : Successfully update stock securities table")


    for i, row in account_info_set.iterrows():
        user_instance = User.objects.get(id=row['user_id'])
        stock_securities_instance = StockSecurities.objects.get(id=row['stock_securities_id'])
        Account.objects.update_or_create(
            id=row['id'],
            defaults={
                'user_id': row['user_id'],
                'account_number': row['account_number'],
                'account_name': row['account_name'],
                'stock_securities_id': row['stock_securities_id'],
                'account_total_investment_principal': row['account_total_investment_principal'],
                'create_time': row['create_time'],
            }
        )

    print(f"{datetime.now()} : Successfully update account table")
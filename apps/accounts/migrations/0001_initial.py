# Generated by Django 4.1.1 on 2022-09-17 14:07

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(help_text='휴대폰 번호는 다음과 같은 형식으로 입력해주세요 : 010-1234-5678', max_length=13, unique=True, validators=[django.core.validators.RegexValidator(regex='^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')])),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자 목록',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.IntegerField(verbose_name='계좌번호')),
                ('account_name', models.CharField(max_length=10, verbose_name='계좌명')),
                ('account_total_investment_principal', models.PositiveIntegerField(verbose_name='계좌별 투자 원금')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='계좌 생성 날짜')),
            ],
            options={
                'verbose_name': '계좌',
                'verbose_name_plural': '계좌 목록',
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='StockSecurities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='증권사')),
            ],
            options={
                'verbose_name': '증권사',
                'verbose_name_plural': '증권사 목록',
                'db_table': 'stock_securities',
            },
        ),
    ]

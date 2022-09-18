# Generated by Django 4.1.1 on 2022-09-18 01:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('investments', '0001_initial'),
        ('stocks', '0001_initial'),
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='investment',
            field=models.ManyToManyField(blank=True, related_name='investment_account', through='investments.Investment', to='stocks.stock', verbose_name='투자내역'),
        ),
        migrations.AddField(
            model_name='account',
            name='stock_securities',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_stock_securities', to='accounts.stocksecurities'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]

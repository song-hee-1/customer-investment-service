# Generated by Django 4.1.1 on 2022-09-17 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='자산군')),
            ],
            options={
                'verbose_name': '증권 자산그룹',
                'verbose_name_plural': '증권 자산그룹 목록',
                'db_table': 'asset_group',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('isin', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='ISIN')),
                ('stock_name', models.CharField(max_length=20, verbose_name='종목명')),
                ('current_price', models.PositiveIntegerField(verbose_name='현재가')),
                ('asset_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_asset_group', to='stocks.assetgroup')),
            ],
            options={
                'verbose_name': '증권',
                'verbose_name_plural': '증권 목록',
                'db_table': 'stock',
            },
        ),
    ]

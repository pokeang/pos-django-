# Generated by Django 3.2.9 on 2021-12-26 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreceipthistorydetail',
            name='daily_receipt_history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_receipt_histories', to='inventory_management.dailyreceipthistory'),
        ),
    ]

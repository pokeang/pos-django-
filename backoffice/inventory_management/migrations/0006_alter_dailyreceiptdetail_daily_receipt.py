# Generated by Django 3.2.9 on 2021-12-30 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0005_alter_dailyreceiptdetail_daily_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreceiptdetail',
            name='daily_receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_receipt_items', to='inventory_management.dailyreceipt'),
        ),
    ]
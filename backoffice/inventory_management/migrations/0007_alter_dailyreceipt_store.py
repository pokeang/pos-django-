# Generated by Django 3.2.9 on 2021-12-30 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
        ('inventory_management', '0006_alter_dailyreceiptdetail_daily_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreceipt',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='settings.store'),
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-12 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('item', '0001_initial'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyReceiptHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sold', models.DateTimeField(auto_now_add=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.store')),
            ],
            options={
                'db_table': 'daily_receipt_history_tbl',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_purchase', models.DateField()),
                ('expected_date', models.DateField()),
                ('status', models.IntegerField(blank=True, choices=[(0, ''), (1, 'Closed'), (2, 'Pending'), (3, 'Cancel')], default=0)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'purchase_order_tbl',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=12)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website', models.CharField(blank=True, max_length=50)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=45)),
                ('postal_code', models.CharField(blank=True, max_length=45)),
                ('country', models.CharField(default='Cambodia', max_length=45)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'supplier_tbl',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('purchase_cost', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('purchase_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory_management.purchaseorder')),
            ],
            options={
                'db_table': 'purchase_order_item_tbl',
            },
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_management.supplier'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='to_store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.store'),
        ),
        migrations.CreateModel(
            name='InventoryCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=500)),
                ('store', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='settings.store')),
                ('storeItem', models.ManyToManyField(to='item.StoreItem')),
            ],
            options={
                'db_table': 'inventory_count_tbl',
            },
        ),
        migrations.CreateModel(
            name='DailyReceiptHistoryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_sold', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('daily_receipt_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_management.dailyreceipthistory')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='item.discount')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.tax')),
            ],
            options={
                'db_table': 'daily_receipt_history_detail_tbl',
            },
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-12 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCardInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('expiration_date', models.DateField()),
                ('cvv', models.IntegerField()),
            ],
            options={
                'db_table': 'credit_card_info_tbl',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'payment_tbl',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=12)),
                ('address', models.TextField(max_length=150)),
                ('description', models.TextField(blank=True, max_length=200)),
            ],
            options={
                'db_table': 'store_tbl',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=8)),
                ('type', models.IntegerField(choices=[(1, 'Included in the price'), (2, 'Added to the price')])),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.store')),
            ],
            options={
                'db_table': 'tax_tbl',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('printed_receipt_img_logo', models.ImageField(upload_to='receipt')),
                ('header_text', models.CharField(max_length=45)),
                ('footer_text', models.CharField(max_length=45)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.store')),
            ],
            options={
                'db_table': 'receipt_tbl',
            },
        ),
    ]

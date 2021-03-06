# Generated by Django 3.2.9 on 2021-12-12 23:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'category_tbl',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=85)),
                ('display', models.BooleanField(default=True)),
                ('price', models.PositiveIntegerField()),
                ('cost', models.PositiveIntegerField(blank=True, null=True)),
                ('bar_code', models.CharField(blank=True, max_length=20, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='item')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.category')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.tax')),
            ],
            options={
                'db_table': 'item_tbl',
            },
        ),
        migrations.CreateModel(
            name='StoreItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('in_stock', models.PositiveIntegerField(blank=True, default=0)),
                ('low_stock', models.PositiveIntegerField(blank=True, default=0)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='item.item')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_items', to='settings.store')),
            ],
            options={
                'db_table': 'store_item_tbl',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('type', models.PositiveIntegerField(choices=[(1, 'Amount'), (2, 'Percentage')], default=1)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.store')),
            ],
            options={
                'db_table': 'discount_tbl',
            },
        ),
    ]

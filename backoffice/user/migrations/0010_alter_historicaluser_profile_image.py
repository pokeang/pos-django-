# Generated by Django 3.2.9 on 2021-12-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_historicaluser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='profile_image',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-16 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211216_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fb_name',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]

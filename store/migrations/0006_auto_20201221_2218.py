# Generated by Django 3.1.2 on 2020-12-21 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20201221_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default='incomplete', max_length=100),
        ),
    ]

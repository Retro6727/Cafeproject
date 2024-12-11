# Generated by Django 4.2.16 on 2024-11-19 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_orderitem_quantity_alter_transactions_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='ordername',
            new_name='items',
        ),
        migrations.AlterField(
            model_name='transactions',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 19, 15, 5, 32, 340192)),
        ),
    ]

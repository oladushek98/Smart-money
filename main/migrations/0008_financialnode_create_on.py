# Generated by Django 2.2 on 2019-04-28 18:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190428_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialnode',
            name='create_on',
            field=models.DateField(default=datetime.date(2019, 3, 31)),
        ),
    ]

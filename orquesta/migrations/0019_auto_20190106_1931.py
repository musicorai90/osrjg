# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-06 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0018_auto_20190106_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='status',
            field=models.CharField(default='E', max_length=1),
        ),
    ]

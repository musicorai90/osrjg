# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-06 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0019_auto_20190106_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='nota',
            field=models.CharField(default=None, max_length=3),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-03 03:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0025_auto_20190302_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
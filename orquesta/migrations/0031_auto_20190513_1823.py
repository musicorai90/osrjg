# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-13 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0030_auto_20190512_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='telefono',
            field=models.BigIntegerField(),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-03 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0016_auto_20190101_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesor',
            name='foto',
            field=models.ImageField(default='fotos/profile.png', upload_to='fotos'),
        ),
    ]

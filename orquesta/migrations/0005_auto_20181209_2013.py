# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-10 00:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0004_fotos'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Fotos',
        ),
        migrations.AddField(
            model_name='admin',
            name='foto',
            field=models.FileField(default='profile.png', upload_to=''),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-16 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0036_remove_actividad_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='urlvideo',
            field=models.TextField(default='hola'),
            preserve_default=False,
        ),
    ]

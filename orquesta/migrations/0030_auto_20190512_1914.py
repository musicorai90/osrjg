# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-12 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orquesta', '0029_auto_20190512_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='cedula',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='nota_aud',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='telefono',
            field=models.IntegerField(),
        ),
    ]

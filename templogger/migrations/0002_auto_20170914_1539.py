# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templogger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperatura',
            name='data',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temperatura',
            name='data_pesquisa',
            field=models.DateTimeField(),
        ),
    ]
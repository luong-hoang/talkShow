# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talkShow', '0003_auto_20171112_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talkshow',
            name='date',
            field=models.DateField(),
        ),
    ]

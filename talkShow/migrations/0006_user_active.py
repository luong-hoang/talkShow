# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talkShow', '0005_auto_20171112_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

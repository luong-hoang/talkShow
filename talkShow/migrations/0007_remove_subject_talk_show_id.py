# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 04:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talkShow', '0006_user_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='talk_show_id',
        ),
    ]

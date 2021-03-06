# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talkShow', '0004_auto_20171112_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talkshowsubject',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='talkShow.Subject'),
        ),
        migrations.AlterField(
            model_name='talkshowsubject',
            name='talk_show_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='talkShow.TalkShow'),
        ),
        migrations.AlterField(
            model_name='talkshowsubject',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='talkShow.User'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField()),
                ('date_modified', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TalkShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TalkShowSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talkShow.Subject')),
                ('talk_show_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talkShow.TalkShow')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='talkshowsubject',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talkShow.User'),
        ),
        migrations.AddField(
            model_name='subject',
            name='talk_show_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='talkShow.TalkShow'),
        ),
        migrations.AddField(
            model_name='subject',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talkShow.User'),
        ),
    ]

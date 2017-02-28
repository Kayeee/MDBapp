# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-27 01:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MDB', '0004_auto_20170214_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='task_id',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor_email',
            field=models.EmailField(default='', max_length=255, verbose_name='Instructor email'),
        ),
        migrations.AlterField(
            model_name='event',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 6, 1, 41, 12, 516635)),
        ),
    ]

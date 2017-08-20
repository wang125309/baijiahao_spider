# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='origin',
            field=models.CharField(default=datetime.date(2017, 8, 19), max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='origin_id',
            field=models.CharField(default=datetime.date(2017, 8, 19), max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='origin_user_id',
            field=models.CharField(default=datetime.date(2017, 8, 19), max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='related_id',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
    ]

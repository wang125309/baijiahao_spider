# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20170820_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='url',
            field=models.CharField(default=datetime.date(2017, 8, 20), max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userresource',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

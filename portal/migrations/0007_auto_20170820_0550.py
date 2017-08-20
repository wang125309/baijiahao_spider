# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_userresource'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresource',
            name='op_url',
            field=models.CharField(default=datetime.date(2017, 8, 20), max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userresource',
            name='op_user',
            field=models.CharField(default=datetime.date(2017, 8, 20), max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userresource',
            name='type',
            field=models.ForeignKey(to='portal.Type', null=True),
            preserve_default=True,
        ),
    ]

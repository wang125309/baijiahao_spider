# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20170819_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='title',
            field=models.CharField(max_length=512),
        ),
    ]

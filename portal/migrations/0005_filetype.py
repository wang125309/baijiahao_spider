# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20170819_0916'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filePath', models.CharField(max_length=512)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(to='portal.Type', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

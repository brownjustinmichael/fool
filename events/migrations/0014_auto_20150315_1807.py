# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20150314_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(default='', max_length=255),
            preserve_default=True,
        ),
    ]

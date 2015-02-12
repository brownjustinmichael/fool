# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150208_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtrigger',
            name='conditions',
            field=models.CharField(default='', blank=True, max_length=256),
            preserve_default=True,
        ),
    ]

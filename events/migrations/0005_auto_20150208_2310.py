# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150208_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtrigger',
            name='blocking',
        ),
        migrations.AddField(
            model_name='event',
            name='blocking',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

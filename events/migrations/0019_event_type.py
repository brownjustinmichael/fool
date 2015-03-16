# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_event_canshuffle'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(max_length=16, default='event'),
            preserve_default=False,
        ),
    ]

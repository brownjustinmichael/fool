# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_remove_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tolog',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_npc'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtrigger',
            name='content',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]

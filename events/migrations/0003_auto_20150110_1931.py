# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_npc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtrigger',
            name='resolved',
        ),
        migrations.AddField(
            model_name='eventtrigger',
            name='result',
            field=models.CharField(blank=True, default='resolve', max_length=8, choices=[('resolve', 'Resolve'), ('switch', 'Switch')], null=True),
            preserve_default=True,
        ),
    ]

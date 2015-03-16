# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20150315_2104'),
        ('events', '0018_event_canshuffle'),
        ('locations', '0006_auto_20150314_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='event_ptr',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('events.event',),
        ),
    ]

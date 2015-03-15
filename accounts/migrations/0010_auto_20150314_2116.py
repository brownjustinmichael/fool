# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20150314_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeevent',
            name='event',
            field=models.ForeignKey(to='events.Event', related_name='_unused_activeevent_event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='event',
            field=models.ForeignKey(to='events.Event', blank=True, related_name='_unused_log_event', null=True),
            preserve_default=True,
        ),
    ]

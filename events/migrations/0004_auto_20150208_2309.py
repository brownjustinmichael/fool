# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150110_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtrigger',
            name='blocking',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventtrigger',
            name='event',
            field=models.ForeignKey(blank=True, null=True, related_name='_unused_2', to='events.Event'),
            preserve_default=True,
        ),
    ]

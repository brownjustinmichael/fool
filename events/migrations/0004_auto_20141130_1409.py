# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_eventtrigger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtrigger',
            name='originalEvent',
        ),
        migrations.AddField(
            model_name='eventtrigger',
            name='event',
            field=models.ForeignKey(null=True, to='events.Event', related_name='_unused_2'),
            preserve_default=True,
        ),
    ]

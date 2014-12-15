# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20141130_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtrigger',
            name='originalEvent',
            field=models.ForeignKey(null=True, to='events.Event', related_name='_unused_1'),
            preserve_default=True,
        ),
    ]

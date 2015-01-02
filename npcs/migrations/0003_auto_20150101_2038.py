# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0002_auto_20150101_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='genericEvent',
            field=models.ForeignKey(to='events.Event', null=True, blank=True, related_name='_unused_4'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='genericEvent',
            field=models.ForeignKey(blank=True, related_name='_unused_4', to='events.Event'),
            preserve_default=True,
        ),
    ]

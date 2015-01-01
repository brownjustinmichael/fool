# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('npcs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='npc',
            field=models.ForeignKey(blank=True, null=True, to='npcs.NPC'),
            preserve_default=True,
        ),
    ]

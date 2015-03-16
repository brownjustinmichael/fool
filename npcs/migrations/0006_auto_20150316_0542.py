# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_damageeffect'),
        ('npcs', '0005_auto_20150314_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='genericEvent',
        ),
        migrations.RemoveField(
            model_name='npclink',
            name='card',
        ),
        migrations.AddField(
            model_name='npc',
            name='card',
            field=models.ForeignKey(null=True, to='cards.NPCCard', blank=True),
            preserve_default=True,
        ),
    ]

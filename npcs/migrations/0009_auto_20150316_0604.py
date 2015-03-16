# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_damageeffect'),
        ('npcs', '0008_auto_20150316_0559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='card',
        ),
        migrations.AddField(
            model_name='npc',
            name='card22',
            field=models.ForeignKey(null=True, to='cards.NPCCard', default=None, blank=True),
            preserve_default=True,
        ),
    ]

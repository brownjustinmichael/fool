# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_damageeffect'),
        ('npcs', '0009_auto_20150316_0604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='card22',
        ),
        migrations.AddField(
            model_name='npc',
            name='card',
            field=models.ForeignKey(blank=True, null=True, to='cards.Card', default=None),
            preserve_default=True,
        ),
    ]

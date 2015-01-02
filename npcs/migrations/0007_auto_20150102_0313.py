# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20150102_0212'),
        ('npcs', '0006_auto_20150102_0311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='card',
        ),
        migrations.AddField(
            model_name='npclink',
            name='card',
            field=models.ForeignKey(null=True, blank=True, to='cards.BaseCard'),
            preserve_default=True,
        ),
    ]

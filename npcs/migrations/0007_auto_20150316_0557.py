# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0006_auto_20150316_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='card',
            field=models.ForeignKey(to='cards.NPCCard', default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]

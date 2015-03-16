# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0007_auto_20150316_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='card',
            field=models.ForeignKey(related_name='npc', blank=True, default=None, to='cards.NPCCard', null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0006_npcinstance_life'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='name',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]

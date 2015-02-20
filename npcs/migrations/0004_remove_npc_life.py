# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0003_remove_npcinstance_life'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='life',
        ),
    ]

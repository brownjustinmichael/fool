# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0003_auto_20141130_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='name',
            field=models.CharField(default='Chest', max_length=60),
            preserve_default=False,
        ),
    ]

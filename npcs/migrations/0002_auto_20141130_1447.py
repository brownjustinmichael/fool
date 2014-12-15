# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npc',
            name='charm',
        ),
        migrations.RemoveField(
            model_name='npc',
            name='dash',
        ),
        migrations.RemoveField(
            model_name='npc',
            name='force',
        ),
        migrations.RemoveField(
            model_name='npc',
            name='money',
        ),
        migrations.RemoveField(
            model_name='npc',
            name='power',
        ),
        migrations.RemoveField(
            model_name='npc',
            name='resist',
        ),
        migrations.RemoveField(
            model_name='npc',
            name='wisdom',
        ),
    ]

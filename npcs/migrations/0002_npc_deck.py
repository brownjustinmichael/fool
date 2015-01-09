# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20150104_0422'),
        ('npcs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='deck',
            field=models.ForeignKey(to='cards.Deck', blank=True, null=True),
            preserve_default=True,
        ),
    ]

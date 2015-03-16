# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_damageeffect'),
        ('events', '0021_event_tolog'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='locationDeck',
            field=models.ForeignKey(null=True, blank=True, to='cards.Deck', related_name='event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventtrigger',
            name='npcthreshold',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='deck',
            field=models.ForeignKey(null=True, blank=True, to='cards.Deck', related_name='_unused_event_location'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20150102_0320'),
        ('events', '0002_event_npc'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='deck',
            field=models.ForeignKey(to='cards.Deck', default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]

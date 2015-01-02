# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0005_auto_20150102_0308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='card',
            field=models.ForeignKey(blank=True, null=True, to='cards.BaseCard'),
            preserve_default=True,
        ),
    ]

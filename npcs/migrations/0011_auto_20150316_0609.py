# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0010_auto_20150316_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='card',
            field=models.ForeignKey(null=True, blank=True, default=None, to='cards.BaseCard'),
            preserve_default=True,
        ),
    ]

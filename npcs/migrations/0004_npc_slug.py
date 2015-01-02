# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0003_auto_20150101_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='slug',
            field=models.SlugField(max_length=255, null=True, blank=True, unique=True),
            preserve_default=True,
        ),
    ]

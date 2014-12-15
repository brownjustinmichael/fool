# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0005_auto_20141130_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='npcinstance',
            name='life',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

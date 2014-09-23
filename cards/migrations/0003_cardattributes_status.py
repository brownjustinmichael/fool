# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_cardattributes_modifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardattributes',
            name='status',
            field=models.CharField(default='stash', choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash')], max_length=6),
            preserve_default=True,
        ),
    ]

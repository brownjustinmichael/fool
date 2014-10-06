# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20140928_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(max_length=7, choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash'), ('play', 'Play')], default='stash'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_cardattributes_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardattributes',
            name='status',
            field=models.CharField(default='stash', max_length=7, choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash')]),
        ),
    ]

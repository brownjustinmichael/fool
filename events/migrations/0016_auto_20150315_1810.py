# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20150315_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deck',
            field=models.ForeignKey(blank=True, null=True, to='cards.Deck', related_name='event'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20141002_0526'),
        ('locations', '0002_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='deck',
            field=models.ForeignKey(to='cards.Deck', blank=True, null=True),
            preserve_default=True,
        ),
    ]

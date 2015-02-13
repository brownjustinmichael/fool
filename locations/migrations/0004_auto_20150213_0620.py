# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20150213_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='deck',
            field=models.OneToOneField(to='cards.Deck', blank=True),
            preserve_default=True,
        ),
    ]

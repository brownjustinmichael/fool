# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_location_deck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='deck',
            field=models.OneToOneField(blank=True, null=True, to='cards.Deck'),
        ),
    ]

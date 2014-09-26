# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='canshuffle',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

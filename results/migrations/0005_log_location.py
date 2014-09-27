# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_location_canshuffle'),
        ('results', '0004_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='location',
            field=models.ForeignKey(to='locations.Location', default=1),
            preserve_default=False,
        ),
    ]

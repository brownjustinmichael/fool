# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20150315_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='canshuffle',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

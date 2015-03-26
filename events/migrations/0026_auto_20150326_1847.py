# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_auto_20150326_1501'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventtrigger',
            options={'ordering': ['event', 'threshold', 'template']},
        ),
    ]

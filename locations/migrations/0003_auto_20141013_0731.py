# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20141013_0616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='globaleventtrigger',
            old_name='played',
            new_name='onlyWhenNotPlayed',
        ),
    ]

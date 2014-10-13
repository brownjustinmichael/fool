# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20141013_0731'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventtrigger',
            old_name='played',
            new_name='onlyWhenNotPlayed',
        ),
    ]

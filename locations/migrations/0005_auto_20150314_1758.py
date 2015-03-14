# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_auto_20150213_0620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationtrigger',
            name='event',
        ),
        migrations.RemoveField(
            model_name='locationtrigger',
            name='location',
        ),
        migrations.RemoveField(
            model_name='locationtrigger',
            name='template',
        ),
        migrations.DeleteModel(
            name='LocationTrigger',
        ),
    ]

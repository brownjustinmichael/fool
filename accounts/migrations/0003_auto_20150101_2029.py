# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('accounts', '0002_auto_20141230_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='active_event',
        ),
        migrations.RemoveField(
            model_name='player',
            name='active_location',
        ),
        migrations.AddField(
            model_name='activeevent',
            name='location',
            field=models.ForeignKey(to='locations.Location', null=True),
            preserve_default=True,
        ),
    ]

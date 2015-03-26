# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20150315_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtrigger',
            name='result',
            field=models.CharField(choices=[('resolve', 'Resolve'), ('switch', 'Switch')], default=None, max_length=8, blank=True, null=True),
            preserve_default=True,
        ),
    ]

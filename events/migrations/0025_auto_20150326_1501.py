# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtrigger',
            name='result',
            field=models.CharField(blank=True, default=None, max_length=8, null=True, choices=[('resolve', 'Resolve'), ('switch', 'Switch')]),
            preserve_default=True,
        ),
    ]

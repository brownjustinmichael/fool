# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20141130_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='generic_content',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='generic_resolved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resultcondition',
            name='content',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_eventeffect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtrigger',
            name='failed_content',
        ),
        migrations.AddField(
            model_name='eventtrigger',
            name='helper',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=True,
        ),
    ]

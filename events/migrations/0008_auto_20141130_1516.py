# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_eventtrigger_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultcondition',
            name='fail_result',
        ),
        migrations.AddField(
            model_name='resultcondition',
            name='success',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

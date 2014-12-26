# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20141130_1841'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resultcondition',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='resultcondition',
            name='card',
        ),
        migrations.RemoveField(
            model_name='resultcondition',
            name='event',
        ),
        migrations.RemoveField(
            model_name='resultcondition',
            name='success_result',
        ),
        migrations.DeleteModel(
            name='ResultCondition',
        ),
    ]

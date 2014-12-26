# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_activeevent_resolved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='title',
        ),
        migrations.AlterField(
            model_name='log',
            name='result',
            field=models.ForeignKey(related_name='_unused_log_result', to='events.Event', blank=True, null=True),
            preserve_default=True,
        ),
    ]

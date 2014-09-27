# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_auto_20140927_0849'),
        ('events', '0002_event_resultcondition'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultcondition',
            name='fail_result',
            field=models.ForeignKey(to='results.Result', related_name='_unused_2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resultcondition',
            name='success_result',
            field=models.ForeignKey(to='results.Result', related_name='_unused_1'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resultcondition',
            unique_together=set([('event', 'card')]),
        ),
        migrations.AddField(
            model_name='event',
            name='generic_result',
            field=models.ForeignKey(to='results.Result'),
            preserve_default=True,
        ),
    ]

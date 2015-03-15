# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20150315_1810'),
        ('accounts', '0010_auto_20150314_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deckstatus',
            name='location',
        ),
        migrations.AddField(
            model_name='deckstatus',
            name='event',
            field=models.ForeignKey(blank=True, to='events.Event', null=True),
            preserve_default=True,
        ),
    ]

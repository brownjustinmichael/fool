# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_auto_20141002_0549'),
        ('accounts', '0005_auto_20141005_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='deckstatus',
            name='location',
            field=models.ForeignKey(to='locations.Location', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='deckstatus',
            unique_together=set([('player', 'deck')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20150316_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardstatus',
            name='player',
            field=models.ForeignKey(null=True, blank=True, to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cardstatus',
            name='deck',
            field=models.ForeignKey(null=True, blank=True, to='accounts.DeckStatus'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='cardstatus',
            unique_together=set([('player', 'card')]),
        ),
    ]

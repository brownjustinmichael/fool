# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_deckstatus_initialized'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardstatus',
            name='deck',
            field=models.ForeignKey(default=None, to='accounts.DeckStatus'),
            preserve_default=False,
        ),
    ]

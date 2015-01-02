# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150102_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardstatus',
            name='deck',
            field=models.ForeignKey(to='accounts.DeckStatus', null=True, blank=True),
            preserve_default=True,
        ),
    ]

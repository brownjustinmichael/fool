# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20150315_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeevent',
            name='cardStatus',
            field=models.ForeignKey(null=True, to='accounts.CardStatus', blank=True),
            preserve_default=True,
        ),
    ]

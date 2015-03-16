# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20150315_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeevent',
            name='cardStatus',
            field=models.ForeignKey(blank=True, null=True, related_name='activeEvent', to='accounts.CardStatus'),
            preserve_default=True,
        ),
    ]

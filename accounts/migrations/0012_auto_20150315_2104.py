# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20150315_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeevent',
            name='cardStatus',
            field=models.OneToOneField(related_name='activeEvent', blank=True, null=True, to='accounts.CardStatus'),
            preserve_default=True,
        ),
    ]

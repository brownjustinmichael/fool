# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150101_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeevent',
            name='cardStatus',
            field=models.ForeignKey(to='accounts.CardStatus', related_name='activeEvent'),
            preserve_default=True,
        ),
    ]

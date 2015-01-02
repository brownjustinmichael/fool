# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150102_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeevent',
            name='cardStatus',
            field=models.OneToOneField(related_name='activeEvent', to='accounts.CardStatus'),
            preserve_default=True,
        ),
    ]

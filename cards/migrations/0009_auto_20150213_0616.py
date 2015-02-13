# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_auto_20150213_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecard',
            name='deck',
            field=models.ForeignKey(to='cards.Deck', null=True, blank=True),
            preserve_default=True,
        ),
    ]

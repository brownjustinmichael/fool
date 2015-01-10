# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20150104_0422'),
        ('accounts', '0002_auto_20150104_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='card',
            field=models.ForeignKey(null=True, default=None, blank=True, to='cards.BaseCard'),
            preserve_default=True,
        ),
    ]

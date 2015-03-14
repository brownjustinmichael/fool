# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20150213_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='temporary',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20141226_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='result',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

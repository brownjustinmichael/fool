# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20141013_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='effect',
            name='name',
            field=models.CharField(default='Effect', max_length=60),
            preserve_default=True,
        ),
    ]

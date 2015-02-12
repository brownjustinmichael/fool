# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20150104_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='basecard',
            name='name',
            field=models.CharField(max_length=60, default=''),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20141130_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeevent',
            name='resolved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

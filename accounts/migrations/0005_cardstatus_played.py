# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20141013_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardstatus',
            name='played',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]

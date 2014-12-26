# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_newcardresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='resolved',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]

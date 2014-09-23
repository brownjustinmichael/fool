# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardattributes',
            name='modifier',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

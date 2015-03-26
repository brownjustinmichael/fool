# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0013_auto_20150326_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flageffect',
            name='flag',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20141002_0526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='status',
        ),
    ]

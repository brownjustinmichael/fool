# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140921_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='content',
        ),
    ]

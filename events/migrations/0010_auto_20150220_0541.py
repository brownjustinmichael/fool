# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_eventtrigger_localonly'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventtrigger',
            options={'ordering': ['event', 'template', 'threshold']},
        ),
    ]

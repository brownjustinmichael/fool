# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150210_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activeevent',
            name='failed',
        ),
        migrations.RemoveField(
            model_name='triggerlog',
            name='success',
        ),
    ]

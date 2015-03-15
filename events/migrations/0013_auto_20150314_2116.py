# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20150314_2116'),
        ('events', '0012_auto_20150314_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationtrigger',
            name='eventtrigger_ptr',
        ),
        migrations.RemoveField(
            model_name='locationtrigger',
            name='location',
        ),
        migrations.DeleteModel(
            name='LocationTrigger',
        ),
    ]

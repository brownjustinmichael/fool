# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20141130_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtrigger',
            name='originalEvent',
            field=models.ForeignKey(null=True, to='events.Event'),
            preserve_default=True,
        ),
    ]

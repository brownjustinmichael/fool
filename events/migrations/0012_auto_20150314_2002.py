# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_locationtrigger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtrigger',
            name='originalEvent',
            field=models.ForeignKey(to='events.Event', null=True, blank=True),
            preserve_default=True,
        ),
    ]

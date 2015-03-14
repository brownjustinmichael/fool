# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20150314_1758'),
        ('events', '0010_auto_20150220_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationTrigger',
            fields=[
                ('eventtrigger_ptr', models.OneToOneField(serialize=False, to='events.EventTrigger', primary_key=True, auto_created=True, parent_link=True)),
                ('location', models.ForeignKey(to='locations.Location')),
            ],
            options={
            },
            bases=('events.eventtrigger',),
        ),
    ]

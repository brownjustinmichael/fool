# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_type'),
        ('locations', '0007_auto_20150315_2121'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='events.Event', primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=('events.event',),
        ),
    ]

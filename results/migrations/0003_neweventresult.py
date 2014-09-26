# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event'),
        ('results', '0002_auto_20140926_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewEventResult',
            fields=[
                ('result_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='results.Result')),
                ('new_event', models.ForeignKey(related_name='_unused_3', to='events.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
    ]

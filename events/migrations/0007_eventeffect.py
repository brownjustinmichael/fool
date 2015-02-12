# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_auto_20150212_0532'),
        ('events', '0006_eventtrigger_conditions'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventEffect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('effect', models.ForeignKey(to='cards.Effect')),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

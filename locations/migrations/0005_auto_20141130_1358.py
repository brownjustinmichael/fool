# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_effect_name'),
        ('events', '0002_auto_20141013_0058'),
        ('locations', '0004_auto_20141013_0732'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationTrigger',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('threshold', models.IntegerField(default=0)),
                ('onlyWhenNotPlayed', models.BooleanField(default=False)),
                ('event', models.ForeignKey(to='events.Event')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('template', models.ForeignKey(to='cards.CardTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='eventtrigger',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventtrigger',
            name='location',
        ),
        migrations.RemoveField(
            model_name='eventtrigger',
            name='template',
        ),
        migrations.DeleteModel(
            name='EventTrigger',
        ),
    ]

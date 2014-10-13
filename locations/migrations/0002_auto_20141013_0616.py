# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_effect_name'),
        ('events', '0002_auto_20141013_0058'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalEventTrigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('threshold', models.IntegerField(default=0)),
                ('played', models.BooleanField(default=False)),
                ('event', models.ForeignKey(to='events.Event')),
                ('template', models.ForeignKey(to='cards.CardTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventtrigger',
            name='played',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

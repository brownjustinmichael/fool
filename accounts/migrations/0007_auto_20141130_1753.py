# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20141130_1753'),
        ('accounts', '0006_auto_20141013_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('stackOrder', models.IntegerField()),
                ('cardStatus', models.ForeignKey(to='accounts.CardStatus')),
                ('event', models.ForeignKey(to='events.Event')),
                ('player', models.ForeignKey(to='accounts.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='activeevent',
            unique_together=set([('player', 'event', 'stackOrder')]),
        ),
    ]

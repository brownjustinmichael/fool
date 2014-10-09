# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20140928_2151'),
        ('cards', '0004_remove_card_status'),
        ('locations', '0004_auto_20141002_0549'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTrigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('threshold', models.IntegerField(default=0)),
                ('event', models.ForeignKey(to='events.Event')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('template', models.ForeignKey(to='cards.CardTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

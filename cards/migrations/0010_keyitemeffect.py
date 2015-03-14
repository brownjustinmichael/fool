# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20150314_2041'),
        ('cards', '0009_auto_20150213_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyItemEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='cards.Effect', auto_created=True)),
                ('keyitem', models.ForeignKey(to='accounts.KeyItem')),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
        ),
    ]

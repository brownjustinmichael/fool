# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_effect_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusChangeEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(to='cards.Effect', auto_created=True, primary_key=True, parent_link=True, serialize=False)),
                ('stat', models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')], max_length=8)),
                ('strength', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
        ),
    ]

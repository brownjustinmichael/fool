# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0010_keyitemeffect'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamageEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, to='cards.Effect', auto_created=True)),
                ('number', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
        ),
    ]

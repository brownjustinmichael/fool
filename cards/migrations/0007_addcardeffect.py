# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_auto_20150212_0611'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddCardEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, to='cards.Effect', serialize=False)),
                ('card', models.ForeignKey(to='cards.BaseCard')),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
        ),
    ]

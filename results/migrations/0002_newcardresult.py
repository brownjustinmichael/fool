# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_effect_name'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewCardResult',
            fields=[
                ('result_ptr', models.OneToOneField(parent_link=True, serialize=False, to='results.Result', auto_created=True, primary_key=True)),
                ('modifier', models.IntegerField(default=0)),
                ('template', models.ForeignKey(related_name='_unused_4', to='cards.CardTemplate')),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
    ]

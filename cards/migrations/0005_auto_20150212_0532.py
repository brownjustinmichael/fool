# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150210_0859'),
        ('cards', '0004_auto_20150211_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlagEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(primary_key=True, serialize=False, to='cards.Effect', parent_link=True, auto_created=True)),
                ('value', models.IntegerField(default=0)),
                ('flag', models.ForeignKey(to='accounts.Flag')),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
        ),
        migrations.RenameModel(
            old_name='StatusChangeEffect',
            new_name='StatChangeEffect',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('stackOrder', models.IntegerField()),
                ('resolved', models.BooleanField(default=False)),
                ('failed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('status', models.CharField(choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash'), ('play', 'Play')], default='stash', max_length=7)),
                ('position', models.IntegerField()),
                ('played', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['status', 'position'],
                'verbose_name_plural': 'Card statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeckStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('initialized', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Deck statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('logged', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['logged'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('force', models.IntegerField(default=0)),
                ('dash', models.IntegerField(default=0)),
                ('resist', models.IntegerField(default=0)),
                ('charm', models.IntegerField(default=0)),
                ('wisdom', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TriggerLog',
            fields=[
                ('log_ptr', models.OneToOneField(to='accounts.Log', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
                ('success', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.log',),
        ),
    ]

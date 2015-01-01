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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.CharField(max_length=7, default='stash', choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash'), ('play', 'Play')])),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Deck statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('log_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='accounts.Log')),
                ('success', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.log',),
        ),
    ]

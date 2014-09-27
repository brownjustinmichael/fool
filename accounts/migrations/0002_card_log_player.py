# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('modifier', models.IntegerField()),
                ('status', models.CharField(max_length=7, default='stash', choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('logged', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
    ]

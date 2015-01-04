# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
        ('locations', '0001_initial'),
        ('accounts', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('force', models.IntegerField(default=0)),
                ('dash', models.IntegerField(default=0)),
                ('resist', models.IntegerField(default=0)),
                ('charm', models.IntegerField(default=0)),
                ('wisdom', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(null=True, max_length=255, blank=True, unique=True)),
                ('life', models.IntegerField()),
                ('genericEvent', models.ForeignKey(null=True, blank=True, to='events.Event', related_name='_unused_4')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NPCInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('life', models.IntegerField(default=0)),
                ('npc', models.ForeignKey(to='npcs.NPC')),
                ('player', models.ForeignKey(to='accounts.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NPCLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('card', models.ForeignKey(null=True, blank=True, to='cards.BaseCard')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('npc', models.ForeignKey(to='npcs.NPC')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='npcinstance',
            unique_together=set([('player', 'npc')]),
        ),
    ]

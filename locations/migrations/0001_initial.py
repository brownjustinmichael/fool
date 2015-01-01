# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def loadLocations (apps, schema_editor):
    Location = apps.get_model ("locations", "Location")
    db_alias = schema_editor.connection.alias
    
    Location.objects.create (title = "Home", slug = "home", description = "It's not much, but it's home.", canshuffle = True)

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalEventTrigger',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('threshold', models.IntegerField(default=0)),
                ('onlyWhenNotPlayed', models.BooleanField(default=False)),
                ('event', models.ForeignKey(to='events.Event')),
                ('template', models.ForeignKey(to='cards.CardTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('canshuffle', models.BooleanField(default=False)),
                ('deck', models.OneToOneField(blank=True, null=True, to='cards.Deck')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationTrigger',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('threshold', models.IntegerField(default=0)),
                ('onlyWhenNotPlayed', models.BooleanField(default=False)),
                ('content', models.TextField(default='')),
                ('event', models.ForeignKey(to='events.Event')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('template', models.ForeignKey(to='cards.CardTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython (loadLocations),
    ]

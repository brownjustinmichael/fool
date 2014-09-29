# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def loadLocations (apps, schema_editor):
    Location = apps.get_model ("locations", "Location")
    db_alias = schema_editor.connection.alias
    
    Location.objects.create (title = "Home", slug = "home", description = "It's not much, but it's home.", canshuffle = True)

class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('canshuffle', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.RunPython (loadLocations),
    ]

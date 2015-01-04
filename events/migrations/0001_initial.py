# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('auto', models.BooleanField(default=False)),
                ('deck', models.ForeignKey(null=True, blank=True, to='cards.Deck')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventTrigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('threshold', models.IntegerField(default=0)),
                ('onlyWhenNotPlayed', models.BooleanField(default=False)),
                ('content', models.TextField(default='', blank=True)),
                ('failed_content', models.TextField(default='', blank=True)),
                ('resolved', models.BooleanField(default=True)),
                ('event', models.ForeignKey(null=True, to='events.Event', related_name='_unused_2')),
                ('originalEvent', models.ForeignKey(null=True, to='events.Event')),
                ('template', models.ForeignKey(to='cards.CardTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='generic_result',
            field=models.ForeignKey(null=True, blank=True, default=None, to='events.EventTrigger', related_name='_unused_event_result'),
            preserve_default=True,
        ),
    ]

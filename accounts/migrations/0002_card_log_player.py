# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
        ('events', '__first__'),
        ('locations', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('results', '__first__'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('logged', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('result', models.ForeignKey(to='results.Result')),
            ],
            options={
                'ordering': ['logged'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('force', models.IntegerField(default=0)),
                ('dash', models.IntegerField(default=0)),
                ('resist', models.IntegerField(default=0)),
                ('charm', models.IntegerField(default=0)),
                ('wisdom', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
                ('active_event', models.ForeignKey(to='events.Event', null=True, blank=True)),
                ('active_location', models.ForeignKey(to='locations.Location', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='player',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
    ]

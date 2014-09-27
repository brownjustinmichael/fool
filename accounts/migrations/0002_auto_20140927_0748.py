# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0002_location'),
        ('cards', '0002_cardtemplate'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('modifier', models.IntegerField()),
                ('status', models.CharField(choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash')], max_length=7, default='stash')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('force', models.IntegerField(default=0)),
                ('dash', models.IntegerField(default=0)),
                ('resist', models.IntegerField(default=0)),
                ('charm', models.IntegerField(default=0)),
                ('wisdom', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
                ('active_event', models.ForeignKey(null=True, to='events.Event', blank=True)),
                ('active_location', models.ForeignKey(null=True, to='locations.Location', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
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

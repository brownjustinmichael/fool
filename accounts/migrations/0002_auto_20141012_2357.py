# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('locations', '0001_initial'),
        ('events', '0001_initial'),
        ('cards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='active_event',
            field=models.ForeignKey(null=True, to='events.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='active_location',
            field=models.ForeignKey(null=True, to='locations.Location', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='deck',
            field=models.OneToOneField(null=True, related_name='player', to='cards.Deck', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='event',
            field=models.ForeignKey(to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='location',
            field=models.ForeignKey(to='locations.Location'),
            preserve_default=True,
        ),
    ]

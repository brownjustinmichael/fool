# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_event_resultcondition'),
        ('accounts', '0002_card_log_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='active_event',
            field=models.ForeignKey(null=True, blank=True, to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='active_location',
            field=models.ForeignKey(null=True, blank=True, to='locations.Location'),
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

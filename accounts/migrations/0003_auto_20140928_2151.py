# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_log_player'),
        ('cards', '0002_auto_20140928_2151'),
        ('events', '0002_event_resultcondition'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='active_event',
            field=models.ForeignKey(blank=True, to='events.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='active_location',
            field=models.ForeignKey(blank=True, to='locations.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='deck',
            field=models.OneToOneField(blank=True, to='cards.Deck', null=True),
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

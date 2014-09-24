# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_event'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('accepted_eula', models.BooleanField(default=False)),
                ('favorite_animal', models.CharField(max_length=20, default='Dragons')),
                ('force', models.IntegerField(default=0)),
                ('dash', models.IntegerField(default=0)),
                ('resist', models.IntegerField(default=0)),
                ('charm', models.IntegerField(default=0)),
                ('wisdom', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('active_event', models.ForeignKey(null=True, blank=True, to='events.Event')),
                ('active_location', models.ForeignKey(null=True, blank=True, to='locations.Location')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

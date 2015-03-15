# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20150314_2116'),
        ('locations', '0005_auto_20150314_1758'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={},
        ),
        migrations.RemoveField(
            model_name='location',
            name='content',
        ),
        migrations.RemoveField(
            model_name='location',
            name='created',
        ),
        migrations.RemoveField(
            model_name='location',
            name='deck',
        ),
        migrations.RemoveField(
            model_name='location',
            name='description',
        ),
        migrations.RemoveField(
            model_name='location',
            name='id',
        ),
        migrations.RemoveField(
            model_name='location',
            name='published',
        ),
        migrations.RemoveField(
            model_name='location',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='location',
            name='title',
        ),
        migrations.AddField(
            model_name='location',
            name='event_ptr',
            field=models.OneToOneField(to='events.Event', default=0, auto_created=True, serialize=False, primary_key=True, parent_link=True),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_remove_location_content'),
        ('accounts', '0003_userprofile_active_scenario'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_location',
            field=models.ForeignKey(null=True, to='locations.Location', blank=True),
            preserve_default=True,
        ),
    ]

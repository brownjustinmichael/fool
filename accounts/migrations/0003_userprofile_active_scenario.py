# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenarios', '0003_scenario'),
        ('accounts', '0002_auto_20140922_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_scenario',
            field=models.ForeignKey(to='scenarios.Scenario', null=True, blank=True),
            preserve_default=True,
        ),
    ]

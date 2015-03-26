# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_flagdependency'),
        ('cards', '0014_remove_flageffect_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flagdependency',
            name='dependent_flag',
        ),
        migrations.RemoveField(
            model_name='flagdependency',
            name='independent_flag',
        ),
        migrations.DeleteModel(
            name='FlagDependency',
        ),
        migrations.AlterUniqueTogether(
            name='logflag',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='logflag',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='logflag',
            name='log',
        ),
        migrations.DeleteModel(
            name='LogFlag',
        ),
        migrations.AlterUniqueTogether(
            name='playerflag',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='playerflag',
            name='flag',
        ),
        migrations.DeleteModel(
            name='Flag',
        ),
        migrations.RemoveField(
            model_name='playerflag',
            name='player',
        ),
        migrations.DeleteModel(
            name='PlayerFlag',
        ),
    ]

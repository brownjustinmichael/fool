# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0001_initial'),
        ('cards', '0012_auto_20150326_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='flageffect',
            name='nflag',
            field=models.ForeignKey(null=True, to='flags.nFlag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flageffect',
            name='flag',
            field=models.ForeignKey(to='accounts.Flag'),
            preserve_default=True,
        ),
    ]

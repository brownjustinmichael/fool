# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_damageeffect'),
        ('flags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flageffect',
            name='flag',
            field=models.ForeignKey(to='flags.nFlag'),
            preserve_default=True,
        ),
    ]

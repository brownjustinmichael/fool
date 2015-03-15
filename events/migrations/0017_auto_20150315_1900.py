# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20150315_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtrigger',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate', blank=True, null=True),
            preserve_default=True,
        ),
    ]

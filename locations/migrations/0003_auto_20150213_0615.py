# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationtrigger',
            name='content',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
    ]

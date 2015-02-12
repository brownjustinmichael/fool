# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_basecard_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecard',
            name='name',
            field=models.CharField(blank=True, max_length=60, default=''),
            preserve_default=True,
        ),
    ]

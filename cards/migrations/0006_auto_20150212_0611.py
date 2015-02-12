# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_auto_20150212_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effectlink',
            name='effect',
            field=models.ForeignKey(to='cards.Effect'),
            preserve_default=True,
        ),
    ]

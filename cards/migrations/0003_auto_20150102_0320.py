# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20150102_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecard',
            name='deck',
            field=models.ForeignKey(blank=True, null=True, to='cards.Deck'),
            preserve_default=True,
        ),
    ]

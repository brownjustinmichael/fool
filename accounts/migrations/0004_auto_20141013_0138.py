# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20141013_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardstatus',
            name='card',
            field=models.ForeignKey(to='cards.BaseCard'),
        ),
    ]

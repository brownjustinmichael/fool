# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_cardattribute2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardattribute2',
            name='card',
        ),
        migrations.RemoveField(
            model_name='cardattribute2',
            name='player',
        ),
        migrations.DeleteModel(
            name='CardAttribute2',
        ),
    ]

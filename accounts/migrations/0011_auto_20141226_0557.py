# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20141226_0518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='result',
            new_name='failed',
        ),
        migrations.AddField(
            model_name='activeevent',
            name='failed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

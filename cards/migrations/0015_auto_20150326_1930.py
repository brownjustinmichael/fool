# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0014_remove_flageffect_flag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flageffect',
            old_name='nflag',
            new_name='flag',
        ),
    ]

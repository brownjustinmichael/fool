# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20140927_1926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ['logged']},
        ),
    ]

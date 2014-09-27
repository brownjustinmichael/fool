# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_cardtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtemplate',
            name='stat',
            field=models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power'), ('money', 'Money')], max_length=8, null=True),
        ),
    ]

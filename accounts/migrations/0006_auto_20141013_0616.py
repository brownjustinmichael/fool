# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_cardstatus_played'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cardstatus',
            options={'ordering': ['status', 'position'], 'verbose_name_plural': 'Card statuses'},
        ),
        migrations.AlterModelOptions(
            name='deckstatus',
            options={'verbose_name_plural': 'Deck statuses'},
        ),
        migrations.AlterField(
            model_name='cardstatus',
            name='played',
            field=models.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_auto_20140927_0849'),
        ('accounts', '0003_auto_20140927_0849'),
        ('cards', '0002_cardtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='result',
            field=models.ForeignKey(to='results.Result'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='player',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_load_players'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(null=True, to='accounts.Deck', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='deck',
            field=models.OneToOneField(null=True, to='accounts.Deck', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='player',
            field=models.ForeignKey(null=True, to='accounts.Player', blank=True),
        ),
    ]

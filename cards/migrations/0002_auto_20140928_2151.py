# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from cards.models import PLAYER_STATS

def loadTemplates (apps, schema_editor):
    Template = apps.get_model ('cards', 'CardTemplate')
    db_alias = schema_editor.connection.alias
    
    Template.objects.using (db_alias).bulk_create ([
        Template (name = stat [1], stat = stat [0]) for stat in PLAYER_STATS
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('modifier', models.IntegerField()),
                ('status', models.CharField(default='stash', max_length=7, choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('stat', models.CharField(blank=True, max_length=8, choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            field=models.ForeignKey(to='cards.Deck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
        migrations.RunPython (loadTemplates,
        )
    ]

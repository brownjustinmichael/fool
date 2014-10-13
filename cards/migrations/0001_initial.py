# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from cards.models import PLAYER_STATS, StatTemplate

def loadTemplates (apps, schema_editor):
    Template = StatTemplate
    db_alias = schema_editor.connection.alias
    
    for stat in PLAYER_STATS:
        Template.objects.create (name = stat [1], stat = stat [0])

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('modifier', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('requiresTarget', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HealEffect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('polymorphic_ctype', models.ForeignKey(null=True, related_name='polymorphic_cards.healeffect_set', editable=False, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('modifier', models.IntegerField()),
                ('deck', models.ForeignKey(to='cards.Deck')),
                ('polymorphic_ctype', models.ForeignKey(null=True, related_name='polymorphic_cards.itemcard_set', editable=False, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('cardtemplate_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='cards.CardTemplate', primary_key=True)),
                ('stat', models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')], max_length=8, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.CreateModel(
            name='PlayerCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('modifier', models.IntegerField()),
                ('experience', models.IntegerField(default=0)),
                ('deck', models.ForeignKey(to='cards.Deck')),
                ('polymorphic_ctype', models.ForeignKey(null=True, related_name='polymorphic_cards.playercard_set', editable=False, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatTemplate',
            fields=[
                ('cardtemplate_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='cards.CardTemplate', primary_key=True)),
                ('stat', models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')], max_length=8, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.AddField(
            model_name='playercard',
            name='template',
            field=models.ForeignKey(to='cards.StatTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemcard',
            name='template',
            field=models.ForeignKey(to='cards.ItemTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='healeffect',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardtemplate',
            name='polymorphic_ctype',
            field=models.ForeignKey(null=True, related_name='polymorphic_cards.cardtemplate_set', editable=False, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(to='cards.Deck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='polymorphic_ctype',
            field=models.ForeignKey(null=True, related_name='polymorphic_cards.card_set', editable=False, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
        migrations.RunPython (loadTemplates),
    ]

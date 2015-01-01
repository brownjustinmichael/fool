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
            name='BaseCard',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('modifier', models.IntegerField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('basecard_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='cards.BaseCard')),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.basecard',),
        ),
        migrations.CreateModel(
            name='CardTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=60, default='Effect')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EffectLink',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HealEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='cards.Effect')),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
        ),
        migrations.CreateModel(
            name='ItemCard',
            fields=[
                ('basecard_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='cards.BaseCard')),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.basecard',),
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('cardtemplate_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='cards.CardTemplate')),
                ('stat', models.CharField(max_length=8, blank=True, choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.CreateModel(
            name='PlayerCard',
            fields=[
                ('basecard_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='cards.BaseCard')),
                ('experience', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.basecard',),
        ),
        migrations.CreateModel(
            name='StatTemplate',
            fields=[
                ('cardtemplate_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='cards.CardTemplate')),
                ('stat', models.CharField(max_length=8, blank=True, choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.CreateModel(
            name='StatusChangeEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='cards.Effect')),
                ('stat', models.CharField(max_length=8, choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')])),
                ('strength', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
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
            model_name='effectlink',
            name='effect',
            field=models.ForeignKey(to='cards.Effect'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='effectlink',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='effect',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, related_name='polymorphic_cards.effect_set', null=True, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardtemplate',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, related_name='polymorphic_cards.cardtemplate_set', null=True, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basecard',
            name='deck',
            field=models.ForeignKey(to='cards.Deck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basecard',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, related_name='polymorphic_cards.basecard_set', null=True, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.RunPython (loadTemplates),
    ]

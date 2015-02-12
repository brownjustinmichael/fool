# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('modifier', models.IntegerField()),
                ('description', models.TextField(null=True, blank=True)),
                ('name', models.CharField(max_length = 60, default = "", blank = True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('basecard_ptr', models.OneToOneField(to='cards.BaseCard', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.basecard',),
        ),
        migrations.CreateModel(
            name='CardTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(default='Effect', max_length=60)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EffectLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HealEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(to='cards.Effect', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.effect',),
        ),
        migrations.CreateModel(
            name='ItemCard',
            fields=[
                ('basecard_ptr', models.OneToOneField(to='cards.BaseCard', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.basecard',),
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('cardtemplate_ptr', models.OneToOneField(to='cards.CardTemplate', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
                ('statistic', models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')], blank=True, max_length=8)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.CreateModel(
            name='NPCCard',
            fields=[
                ('basecard_ptr', models.OneToOneField(to='cards.BaseCard', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.basecard',),
        ),
        migrations.CreateModel(
            name='NPCTemplate',
            fields=[
                ('cardtemplate_ptr', models.OneToOneField(to='cards.CardTemplate', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.CreateModel(
            name='PlayerCard',
            fields=[
                ('basecard_ptr', models.OneToOneField(to='cards.BaseCard', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
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
                ('cardtemplate_ptr', models.OneToOneField(to='cards.CardTemplate', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
                ('statistic', models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')], blank=True, max_length=8)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.CreateModel(
            name='StatusChangeEffect',
            fields=[
                ('effect_ptr', models.OneToOneField(to='cards.Effect', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
                ('stat', models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power')], max_length=8)),
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
    ]

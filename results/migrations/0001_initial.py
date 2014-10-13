# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewEventResult',
            fields=[
                ('result_ptr', models.OneToOneField(serialize=False, to='results.Result', auto_created=True, parent_link=True, primary_key=True)),
                ('new_event', models.ForeignKey(related_name='_unused_3', to='events.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
        migrations.CreateModel(
            name='EnemyResult',
            fields=[
                ('result_ptr', models.OneToOneField(serialize=False, to='results.Result', auto_created=True, parent_link=True, primary_key=True)),
                ('enemy_name', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
        migrations.CreateModel(
            name='StatResult',
            fields=[
                ('result_ptr', models.OneToOneField(serialize=False, to='results.Result', auto_created=True, parent_link=True, primary_key=True)),
                ('stat', models.CharField(null=True, default=None, max_length=8, choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power'), ('money', 'Money')])),
                ('modifier', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
        migrations.AddField(
            model_name='result',
            name='polymorphic_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType', related_name='polymorphic_results.result_set', editable=False, null=True),
            preserve_default=True,
        ),
    ]

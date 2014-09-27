# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_resultcondition'),
        ('contenttypes', '0001_initial'),
        ('results', '0001_initial'),
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
                ('result_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='results.Result')),
                ('new_event', models.ForeignKey(to='events.Event', related_name='_unused_3')),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
        migrations.CreateModel(
            name='EnemyResult',
            fields=[
                ('result_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='results.Result')),
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
                ('result_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='results.Result')),
                ('stat', models.CharField(max_length=8, default=None, null=True, choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power'), ('money', 'Money')])),
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
            field=models.ForeignKey(null=True, editable=False, to='contenttypes.ContentType', related_name='polymorphic_results.result_set'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('cards', '0004_auto_20140925_0641'),
        ('events', '0002_event'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnemyResult',
            fields=[
                ('result_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='results.Result', serialize=False)),
                ('enemy_name', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
        migrations.CreateModel(
            name='ResultCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('success_threshold', models.IntegerField(default=0)),
                ('card', models.ForeignKey(to='cards.Card')),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatResult',
            fields=[
                ('result_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='results.Result', serialize=False)),
                ('stat', models.CharField(default=None, null=True, choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power'), ('money', 'Money')], max_length=8)),
                ('modifier', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('results.result',),
        ),
        migrations.AddField(
            model_name='resultcondition',
            name='fail_result',
            field=models.ForeignKey(related_name='_unused_2', to='results.Result'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resultcondition',
            name='success_result',
            field=models.ForeignKey(related_name='_unused_1', to='results.Result'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resultcondition',
            unique_together=set([('event', 'card')]),
        ),
        migrations.AddField(
            model_name='result',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, related_name='polymorphic_results.result_set', to='contenttypes.ContentType'),
            preserve_default=True,
        ),
    ]

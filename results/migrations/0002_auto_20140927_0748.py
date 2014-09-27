# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event'),
        ('contenttypes', '0001_initial'),
        ('locations', '0002_location'),
        ('accounts', '0002_auto_20140927_0748'),
        ('cards', '0002_cardtemplate'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('logged', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('location', models.ForeignKey(to='locations.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
                ('result_ptr', models.OneToOneField(parent_link=True, serialize=False, to='results.Result', auto_created=True, primary_key=True)),
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
                ('result_ptr', models.OneToOneField(parent_link=True, serialize=False, to='results.Result', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('success_threshold', models.IntegerField(default=0)),
                ('card', models.ForeignKey(to='cards.CardTemplate')),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatResult',
            fields=[
                ('result_ptr', models.OneToOneField(parent_link=True, serialize=False, to='results.Result', auto_created=True, primary_key=True)),
                ('stat', models.CharField(choices=[('force', 'Force'), ('dash', 'Dash'), ('resist', 'Resist'), ('charm', 'Charm'), ('wisdom', 'Wisdom'), ('power', 'Power'), ('money', 'Money')], null=True, max_length=8, default=None)),
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
            field=models.ForeignKey(to='results.Result', related_name='_unused_2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resultcondition',
            name='success_result',
            field=models.ForeignKey(to='results.Result', related_name='_unused_1'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resultcondition',
            unique_together=set([('event', 'card')]),
        ),
        migrations.AddField(
            model_name='result',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, to='contenttypes.ContentType', related_name='polymorphic_results.result_set'),
            preserve_default=True,
        ),
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
    ]

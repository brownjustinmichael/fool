# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_flagdependency'),
    ]

    operations = [
        migrations.CreateModel(
            name='nFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('temporary', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='nFlagDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('independent_flag_value', models.IntegerField(default=0)),
                ('dependent_flag_value', models.IntegerField(default=0)),
                ('dependent_flag', models.ForeignKey(related_name='_unused_flagdependency_flag', to='flags.nFlag')),
                ('independent_flag', models.ForeignKey(to='flags.nFlag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='nLogFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('state', models.IntegerField(default=0)),
                ('flag', models.ForeignKey(to='flags.nFlag')),
                ('log', models.ForeignKey(to='accounts.Log')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='nPlayerFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('state', models.IntegerField(default=0)),
                ('flag', models.ForeignKey(to='flags.nFlag')),
                ('player', models.ForeignKey(to='accounts.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='nplayerflag',
            unique_together=set([('player', 'flag')]),
        ),
        migrations.AlterUniqueTogether(
            name='nlogflag',
            unique_together=set([('log', 'flag')]),
        ),
    ]

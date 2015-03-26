# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20150326_1902'),
        ('flags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlagDependency',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('independent_flag_value', models.IntegerField(default=0)),
                ('dependent_flag_value', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogFlag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('state', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerFlag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('state', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='nFlag',
            new_name='Flag',
        ),
        migrations.RemoveField(
            model_name='nflagdependency',
            name='dependent_flag',
        ),
        migrations.RemoveField(
            model_name='nflagdependency',
            name='independent_flag',
        ),
        migrations.DeleteModel(
            name='nFlagDependency',
        ),
        migrations.AlterUniqueTogether(
            name='nlogflag',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='nlogflag',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='nlogflag',
            name='log',
        ),
        migrations.DeleteModel(
            name='nLogFlag',
        ),
        migrations.AlterUniqueTogether(
            name='nplayerflag',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='nplayerflag',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='nplayerflag',
            name='player',
        ),
        migrations.DeleteModel(
            name='nPlayerFlag',
        ),
        migrations.AddField(
            model_name='playerflag',
            name='flag',
            field=models.ForeignKey(to='flags.Flag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerflag',
            name='player',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='playerflag',
            unique_together=set([('player', 'flag')]),
        ),
        migrations.AddField(
            model_name='logflag',
            name='flag',
            field=models.ForeignKey(to='flags.Flag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logflag',
            name='log',
            field=models.ForeignKey(to='accounts.Log'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='logflag',
            unique_together=set([('log', 'flag')]),
        ),
        migrations.AddField(
            model_name='flagdependency',
            name='dependent_flag',
            field=models.ForeignKey(to='flags.Flag', related_name='_unused_flagdependency_flag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flagdependency',
            name='independent_flag',
            field=models.ForeignKey(to='flags.Flag'),
            preserve_default=True,
        ),
    ]

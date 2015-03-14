# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_flag_temporary'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KeyItemInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('number', models.IntegerField(default=0)),
                ('keyitem', models.ForeignKey(to='accounts.KeyItem')),
                ('player', models.ForeignKey(to='accounts.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='keyiteminstance',
            unique_together=set([('player', 'keyitem')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150210_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('state', models.IntegerField(default=0)),
                ('flag', models.ForeignKey(to='accounts.Flag')),
                ('log', models.ForeignKey(to='accounts.Log')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='logflag',
            unique_together=set([('log', 'flag')]),
        ),
    ]

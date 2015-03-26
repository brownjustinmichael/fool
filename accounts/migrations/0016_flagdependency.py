# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20150316_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlagDependency',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('independent_flag_value', models.IntegerField(default=0)),
                ('dependent_flag_value', models.IntegerField(default=0)),
                ('dependent_flag', models.ForeignKey(to='accounts.Flag', related_name='_unused_flagdependency_flag')),
                ('independent_flag', models.ForeignKey(to='accounts.Flag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

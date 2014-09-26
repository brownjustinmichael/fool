# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event'),
        ('accounts', '0003_userprofile_money'),
        ('results', '0003_neweventresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('logged', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('result', models.ForeignKey(to='results.Result')),
                ('user', models.ForeignKey(to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

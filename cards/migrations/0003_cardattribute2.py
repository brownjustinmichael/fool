# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_money'),
        ('cards', '0002_card_cardattribute'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardAttribute2',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('modifier', models.IntegerField()),
                ('status', models.CharField(default='stash', max_length=7, choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash')])),
                ('card', models.ForeignKey(to='cards.Card')),
                ('player', models.ForeignKey(to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

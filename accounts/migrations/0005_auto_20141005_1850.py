# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20141002_0526'),
        ('accounts', '0004_auto_20140928_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[('hand', 'Hand'), ('deck', 'Deck'), ('discard', 'Discard'), ('stash', 'Stash'), ('play', 'Play')], default='stash', max_length=7)),
                ('position', models.IntegerField()),
                ('card', models.ForeignKey(to='cards.Card')),
            ],
            options={
                'ordering': ['status', 'position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeckStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('deck', models.ForeignKey(to='cards.Deck')),
                ('player', models.ForeignKey(to='accounts.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cardstatus',
            name='deck',
            field=models.ForeignKey(to='accounts.DeckStatus'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='cardstatus',
            unique_together=set([('deck', 'position', 'status')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='deck',
            field=models.OneToOneField(related_name='player', to='cards.Deck', null=True, blank=True),
        ),
    ]

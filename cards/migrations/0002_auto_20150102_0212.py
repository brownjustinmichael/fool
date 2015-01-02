# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0004_npc_slug'),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPCCard',
            fields=[
                ('basecard_ptr', models.OneToOneField(to='cards.BaseCard', auto_created=True, serialize=False, parent_link=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.basecard',),
        ),
        migrations.CreateModel(
            name='NPCTemplate',
            fields=[
                ('cardtemplate_ptr', models.OneToOneField(to='cards.CardTemplate', auto_created=True, serialize=False, parent_link=True, primary_key=True)),
                ('npc', models.ForeignKey(to='npcs.NPC')),
            ],
            options={
                'abstract': False,
            },
            bases=('cards.cardtemplate',),
        ),
        migrations.AddField(
            model_name='npccard',
            name='template',
            field=models.ForeignKey(to='cards.NPCTemplate'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='itemtemplate',
            old_name='stat',
            new_name='statistic',
        ),
        migrations.RenameField(
            model_name='stattemplate',
            old_name='stat',
            new_name='statistic',
        ),
    ]

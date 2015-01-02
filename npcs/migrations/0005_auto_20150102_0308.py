# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20150102_0212'),
        ('locations', '0001_initial'),
        ('npcs', '0004_npc_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPCLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('location', models.ForeignKey(to='locations.Location')),
                ('npc', models.ForeignKey(to='npcs.NPC')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='npc',
            name='card',
            field=models.ForeignKey(null=True, blank=True, to='cards.NPCCard'),
            preserve_default=True,
        ),
    ]

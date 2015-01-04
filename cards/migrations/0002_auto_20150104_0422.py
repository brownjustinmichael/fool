# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from cards.models import StatTemplate, PLAYER_STATS

def makeTemplates (apps, schema_editor):
    for stat in PLAYER_STATS:
        StatTemplate.objects.create (statistic = stat [0])

class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('npcs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='npctemplate',
            name='npc',
            field=models.ForeignKey(to='npcs.NPC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='npccard',
            name='template',
            field=models.ForeignKey(to='cards.NPCTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemcard',
            name='template',
            field=models.ForeignKey(to='cards.ItemTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='effectlink',
            name='effect',
            field=models.ForeignKey(to='cards.Effect'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='effectlink',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='effect',
            name='polymorphic_ctype',
            field=models.ForeignKey(null=True, editable=False, to='contenttypes.ContentType', related_name='polymorphic_cards.effect_set'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardtemplate',
            name='polymorphic_ctype',
            field=models.ForeignKey(null=True, editable=False, to='contenttypes.ContentType', related_name='polymorphic_cards.cardtemplate_set'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='template',
            field=models.ForeignKey(to='cards.CardTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basecard',
            name='deck',
            field=models.ForeignKey(null=True, blank=True, to='cards.Deck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basecard',
            name='polymorphic_ctype',
            field=models.ForeignKey(null=True, editable=False, to='contenttypes.ContentType', related_name='polymorphic_cards.basecard_set'),
            preserve_default=True,
        ),
        migrations.RunPython (makeTemplates),
    ]

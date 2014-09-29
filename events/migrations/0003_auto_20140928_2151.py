# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from results.models import StatResult, NewEventResult
from events.models import ResultCondition
from events.models import Event
from cards.models import MONEY, FORCE, POWER, CardTemplate

def loadResult (apps, schema_editor):
    null = StatResult.objects.create (name = "Null", message = "Nothing happens.", stat = 'force', modifier = 0)
    
    chest = Event.objects.create (title = "Chest", slug = "chest", description = "You find a large, locked chest.", content = "What's this? A chest? Looks pretty fancy. Pretty ominous looking, too. Probably shouldn't disturb it. There could be anything in there.\n\nBut then again. It's a big, locked chest. There could be anything in there.", generic_result = null)
    
    forcetemplate = CardTemplate.objects.filter (stat = FORCE).first ()
    
    generic_result = NewEventResult.objects.create (name = "No Luck", message = "You gave it your best shot, but it was all for naught. The chest remains there, almost taunting you. Damn. You really wanted to know what was in there. Maybe one more try?", new_event = chest)
    
    force = ResultCondition.objects.create (event = chest, success_result = StatResult.objects.create (name = "Chest Opens", message = "After a lot of prying (and a rather clever use of nearby birdbath), you manage to break the lock and behold... eight bucks. Really? You reckon the chest itself cost more. But well, the chest won't fit in your pocket, so you grab the cash and move along before the owner of that birdbath comes looking for you...", stat = MONEY, modifier = 800), fail_result = generic_result, card = forcetemplate, success_threshold = 5)
    
    chest.generic_result = generic_result
    chest.save ()
    
    powertemplate = CardTemplate.objects.filter (stat = POWER).first ()
    
    pig_result = StatResult.objects.create (name = "Pig Troubles", message = "For some reason, it looks like those were cash munching pigs. You manage to save most of your stuff before they move on, but you lose a few bucks.", stat = MONEY, modifier = -400)
    
    pigs = Event.objects.create (title = "Flying Pigs?", slug = "pigs", description = "Pigs are flying about", content = "", generic_result = pig_result, auto = True)
    
    power = ResultCondition.objects.create (event = chest, success_result = NewEventResult.objects.create (name = "Flying Pigs?", message = "A bit of demonology goes a long way. You feel the power fading from your fingertips. You open the chest... and a herd of pigs come literally flying out. Or would it be a flock? A gaggle?\n\nWhatever. They knock you into the mud, and your pants are soaked.", new_event = pigs), fail_result = generic_result, card = powertemplate, success_threshold = 4)

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_resultcondition'),
        ('results', '0002_auto_20140928_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultcondition',
            name='fail_result',
            field=models.ForeignKey(related_name='_unused_2', to='results.Result'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resultcondition',
            name='success_result',
            field=models.ForeignKey(related_name='_unused_1', to='results.Result'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resultcondition',
            unique_together=set([('event', 'card')]),
        ),
        migrations.AddField(
            model_name='event',
            name='generic_result',
            field=models.ForeignKey(to='results.Result'),
            preserve_default=True,
        ),
        migrations.RunPython (loadResult,)
    ]

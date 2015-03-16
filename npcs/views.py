from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from npcs.models import NPCLink
from cards.models import NPCCard
from accounts.models import Player
from locations.models import Location

@login_required
def npc (request, slug):
    # get the Card object
    # TODO This should really fetch a cardStatus (which should be called a cardInstance)
    print ("HERE I AM")
    
    npcLink = get_object_or_404 (NPCLink, id=slug)
    player = get_object_or_404 (Player, user = request.user)
    # now return the rendered template

    # TODO do this correctly
    slug = request.GET.get ('from', 'index.html').split ("/") [-2]
    location = get_object_or_404 (Location, slug = slug)    
    
    if player.active_event is not None:
        raise RuntimeError ("You can't engage an NPC while there are unresolved events")
    
    print (npcLink.npc)
    print (npcLink.npc.card)
    
    cardStatus = npcLink.npc.card.getStatus (player)
    print ("Playing", cardStatus)
    location.playCard (player, cardStatus)
    print ("We just played", cardStatus, cardStatus.status)
    
    return redirect (request.GET.get ('from', 'index.html'))
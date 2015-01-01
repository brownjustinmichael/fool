from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from locations.models import Location
from accounts.models import Player
from cards.models import CARD_IN_HAND, CARD_IN_PLAY, CARD_IN_DISCARD

@login_required (login_url='/accounts/login/')
def index(request):
    # get the locations that are published
    locations = Location.objects.filter (published=True)
    # now return the rendered template
    player = get_object_or_404 (Player, user = request.user)
    return render (request, 'exploration/index.html', {'locations': locations, 'hand': [card.card for card in player.getCards (CARD_IN_HAND).all ()], 'request': request, 'numcardsindeck': player.deck.getNumCards (player)})

@login_required (login_url='/accounts/login/')
def location (request, slug):
    # get the Location object
    location = get_object_or_404 (Location, slug=slug)
    location_deck = location.deck
    
    # now return the rendered template
    player = get_object_or_404 (Player, user = request.user)
    in_play = player.getCards (CARD_IN_PLAY)
    
    active_location = player.active_location
    
    if location == active_location:
        player.resolve (location)
        
    in_play = player.getCards (CARD_IN_PLAY)
    print ("THE CARDS IN PLAY ARE", in_play)
        
    event = player.resolve (location)
    if event is not None:
        player.active_event = event.event
        player.active_location = location
        player.save ()
        print (player.active_event.title)
    if (event is None):
        print ("THE EVENT IS NONE, RESOLVE ALL CARDS")
        player.active_event = None
        player.active_location = None
        for card in in_play:
            card.resolve ()
    
    in_play = player.getCards (CARD_IN_PLAY)
        
    return render (request, 'exploration/location.html', {'location': location, 'location_deck': location_deck, 'numcardsatlocation': location_deck.getNumCards (player) if location_deck is not None else None, 'in_play': [card.card for card in in_play], 'hand': [card.card for card in player.getCards (CARD_IN_HAND).all ()], 'request': request, 'userprofile': player, 'numcardsindeck': player.deck.getNumCards (player), 'logs': player.log_set.filter (location = location).all ()})

@login_required (login_url='/accounts/login/')
def draw (request, slug):
    # get the Location object
    player = get_object_or_404 (Player, user = request.user)
        
    location = get_object_or_404 (Location, slug=slug)
    location_deck = location.deck
    if (location_deck is not None):
        in_play = player.getCards (CARD_IN_PLAY).all ()
        if location_deck.getNumCards (player, CARD_IN_PLAY) > 0:
            # If there are cards in play, you can't draw a card, duh.
            return redirect (location.get_absolute_url ())
    else:
        in_play = []

    # now return the rendered template
    
    location.trigger_event (player, location_deck.drawCard (player), played = False)
        
    return redirect (location.get_absolute_url ())

@login_required (login_url='/accounts/login/')
def shuffle (request, slug):
    # get the Location object
    player = get_object_or_404 (Player, user = request.user)
    
    # Reset the NPCs when resting. This belongs elsewhere
    for npc in player.npcinstance_set.all ():
        npc.delete ()
        
    location = get_object_or_404 (Location, slug=slug)
    location_deck = location.deck
    if (location_deck is not None):
        if player.getCards (CARD_IN_PLAY).count () > 0:
            # If there are cards in play, you can't draw a card, duh.
            return redirect (location.get_absolute_url ())
    else:
        in_play = []
        return redirect (location.get_absolute_url ())

    # now return the rendered template
    
    location_deck.reshuffle (player)
        
    return redirect (location.get_absolute_url ())

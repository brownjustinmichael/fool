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
    return render (request, 'exploration/index.html', {'locations': locations, 'hand': [card.card for card in player.deck.getCards (player, CARD_IN_HAND).all ()], 'request': request, 'numcardsindeck': player.deck.getNumCards (player)})

@login_required (login_url='/accounts/login/')
def location (request, slug):
    # get the Location object
    location = get_object_or_404 (Location, slug=slug)
    location_deck = location.deck
    if (location_deck is not None):
        in_play = location_deck.getCards (CARD_IN_PLAY)
    else:
        in_play = []
    # now return the rendered template
    player = get_object_or_404 (Player, user = request.user)
    
    event = player.active_event
    if (event is None):
        for card in in_play:
            print (str (card))
            card.discard ()
    active_location = player.active_location
    
    if location == active_location:
        event.resolve (player, location)
        
    return render (request, 'exploration/location.html', {'location': location, 'location_deck': location_deck, 'in_play': in_play, 'hand': [card.card for card in player.deck.getCards (player, CARD_IN_HAND).all ()], 'request': request, 'userprofile': player, 'numcardsindeck': player.deck.getNumCards (player), 'logs': player.log_set.filter (location = location).all ()})

@login_required (login_url='/accounts/login/')
def draw (request, slug):
    print ("DRAWING")
    # get the Location object
    location = get_object_or_404 (Location, slug=slug)
    location_deck = location.deck
    if (location_deck is not None):
        in_play = location_deck.getCards (CARD_IN_PLAY)
        if location_deck.getNumCards (CARD_IN_PLAY) > 0:
            return redirect (location.get_absolute_url ())
    else:
        in_play = []

    # now return the rendered template
    player = get_object_or_404 (Player, user = request.user)
    
    event = player.active_event
    active_location = player.active_location
    
    if location == active_location:
        event.resolve (player, location)
        
    return redirect (location.get_absolute_url ())

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
        
    event = player.resolve (location)
    if (event is None):
        for card in in_play:
            card.resolve ()
    
    in_play = player.getCards (CARD_IN_PLAY)
        
    in_hand = [card.card for card in player.getCards (CARD_IN_HAND).all ()]
    if event is not None:
        in_hand += [card.card for card in event.getCards (player, CARD_IN_HAND)]
        
    return render (request, 'exploration/location.html', {'location': location, 'location_deck': location_deck, 'numcardsatlocation': location_deck.getNumCards (player) if location_deck is not None else None, 'in_play': [card.card for card in in_play], 'hand': in_hand, 'request': request, 'userprofile': player, 'numcardsindeck': player.deck.getNumCards (player), 'logs': player.log_set.filter (location = location).all ()})

@login_required (login_url='/accounts/login/')
def draw (request, slug):
    # get the Location object
    player = get_object_or_404 (Player, user = request.user)
        
    location = get_object_or_404 (Location, slug=slug)

    location.drawCard (player)

    return redirect (location.get_absolute_url ())


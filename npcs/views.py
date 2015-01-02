from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

@login_required (login_url='/accounts/login/')
def npc (request, slug):
    # get the Location object
    location = get_object_or_404 (Location, slug=slug)
    location_deck = location.deck
    
    # now return the rendered template
    player = get_object_or_404 (Player, user = request.user)
    in_play = player.getCards (CARD_IN_PLAY)
    
    active_location = player.active_location
    
    print ("THE ACTIVE LOCATION IS ", active_location)
    
    if location == active_location:
        player.resolve (location)
        
    in_play = player.getCards (CARD_IN_PLAY)
    print ("THE CARDS IN PLAY ARE", in_play)
        
    event = player.resolve (location)
    if (event is None):
        print ("THE EVENT IS NONE, RESOLVE ALL CARDS")
        for card in in_play:
            card.resolve ()
    
    in_play = player.getCards (CARD_IN_PLAY)
        
    return render (request, 'exploration/location.html', {'location': location, 'location_deck': location_deck, 'numcardsatlocation': location_deck.getNumCards (player) if location_deck is not None else None, 'in_play': [card.card for card in in_play], 'hand': [card.card for card in player.getCards (CARD_IN_HAND).all ()], 'request': request, 'userprofile': player, 'numcardsindeck': player.deck.getNumCards (player), 'logs': player.log_set.filter (location = location).all ()})

@login_required
def card (request, slug):
    # get the Card object
    # TODO This should really fetch a cardStatus (which should be called a cardInstance)
    card = get_object_or_404 (BaseCard, id=slug)
    player = get_object_or_404 (Player, user = request.user)
    # now return the rendered template
    deck = get_object_or_404 (Deck, player = player)
    
    location = request.user.player.active_location
    
    event = player.resolve (location)
    
    if event is None:
        slug = request.GET.get ('from', 'index.html')
        location = Location.objects.filter (slug = slug [13:-1]).first ()
        if location is not None:
            location.trigger_event (player, card.getStatus (player), location)
        return redirect (request.GET.get ('from', 'index.html'))
    
    player.resolve (location, card.getStatus (player))
    
    return redirect (request.GET.get ('from', 'index.html'))
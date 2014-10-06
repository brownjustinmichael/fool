from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Player
from cards.models import Card, Deck, CARD_IN_DISCARD, CARD_IN_HAND

@login_required
def card (request, slug):
    # get the Card object
    card = get_object_or_404 (Card, id=slug)
    player = get_object_or_404 (Player, user = request.user)
    # now return the rendered template
    deck = get_object_or_404 (Deck, player = player)
    
    event = request.user.player.active_event
    location = request.user.player.active_location
    if event is None:
        return redirect (request.GET.get ('from', 'index.html'))
    
    event.resolve (player, location, card)
    
    return redirect (request.GET.get ('from', 'index.html'))

@login_required
def draw (request):
    # now return the rendered template
    username = None
    player = get_object_or_404 (Player, user = request.user)
    deck = get_object_or_404 (Deck, player = player)

    card = deck.drawCard (player)
    print ("Drawing " + str (card.template) + str (card.modifier))
    # card.status = CARD_IN_HAND
    # card.save ()
    return redirect (request.GET.get ('from', 'index.html'))

@login_required
def shuffle (request):
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    request.user.player.deck.reshuffle (request.user.player)
    return redirect (request.GET.get ('from', 'index.html'))


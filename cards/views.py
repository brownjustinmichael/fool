from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Card
from accounts.models import CARD_IN_DISCARD, CARD_IN_HAND
from results.models import Log

@login_required
def card (request, slug):
    # get the Card object
    cardattribute = get_object_or_404 (Card, id=slug)
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    # cardattribute.status = CARD_IN_DISCARD
    # cardattribute.save ()
    
    event = request.user.player.active_event
    location = request.user.player.active_location
    if event is None:
        return redirect (request.GET.get ('from', 'index.html'))
    
    try:
        resultcondition = event.resultcondition_set.filter (card = cardattribute.template).all () [0]
        result = resultcondition.checkSuccess (cardattribute)
        print (result.enact (request.user.player))
    except IndexError:
        # Treat this better
        print ("Nothing happens...")
        
    newlog = Log (title = event.title, event = event, result = result, user = request.user.player, location = location)
    newlog.save ()
        
    request.user.player.save ()
    
    return redirect (request.GET.get ('from', 'index.html'))

@login_required
def draw (request):
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    card = request.user.player.drawCard ()
    print ("Drawing " + str (card.template) + str (card.modifier))
    card.status = CARD_IN_HAND
    card.save ()
    return redirect (request.GET.get ('from', 'index.html'))

@login_required
def shuffle (request):
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    request.user.player.reshuffle ()
    return redirect (request.GET.get ('from', 'index.html'))


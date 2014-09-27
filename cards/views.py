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
    cardattribute.status = CARD_IN_DISCARD
    cardattribute.save ()
    
    event = request.user.userprofile.active_event
    
    try:
        resultcondition = event.resultcondition_set.filter (card = cardattribute.card).all () [0]
        result = resultcondition.checkSuccess (cardattribute)
        print (result.enact (request.user.userprofile))
    except IndexError:
        # Treat this better
        print ("Nothing happens...")
        
    newlog = Log (title = event.title, event = event, result = result, user = request.user.userprofile, location = request.user.userprofile.active_location)
    newlog.save ()
        
    request.user.userprofile.save ()
    
    return redirect (request.GET.get ('from', 'index.html'))

@login_required
def draw (request):
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    card = request.user.userprofile.drawCard ()
    print ("Drawing " + str (card.card) + str (card.modifier))
    card.status = CARD_IN_HAND
    card.save ()
    return redirect (request.GET.get ('from', 'index.html'))

@login_required
def shuffle (request):
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    request.user.userprofile.reshuffle ()
    return redirect (request.GET.get ('from', 'index.html'))


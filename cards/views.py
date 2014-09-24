from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cards.models import CardAttribute
from accounts.models import CARD_IN_DISCARD

@login_required
def card (request, slug):
    # get the Location object
    card = get_object_or_404 (CardAttribute, id=slug)
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    card.status = CARD_IN_DISCARD
    card.save ()
    return redirect (request.GET.get ('from', 'index.html'))


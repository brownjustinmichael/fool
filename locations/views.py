from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from locations.models import Location
from accounts.models import Player

@login_required (login_url='/accounts/login/')
def index(request):
    # get the locations that are published
    locations = Location.objects.filter (published=True)
    # now return the rendered template
    player = get_object_or_404 (Player, user = request.user)
    return render (request, 'exploration/index.html', {'locations': locations, 'hand': request.user.userprofile.getCardsInHand (), 'request': request, 'numcardsindeck': request.user.userprofile.getNumCardsInDeck ()})

@login_required (login_url='/accounts/login/')
def location (request, slug):
    # get the Location object
    location = get_object_or_404 (Location, slug=slug)
    # now return the rendered template
    username = None
    if request.user.is_authenticated():
        player = get_object_or_404 (Player, user = request.user)
        return render (request, 'exploration/location.html', {'location': location, 'hand': request.user.userprofile.getCardsInHand (), 'request': request, 'userprofile': request.user.userprofile, 'numcardsindeck': request.user.userprofile.getNumCardsInDeck (), 'logs': request.user.userprofile.log_set.filter (location = location).order_by ('logged').all ()})

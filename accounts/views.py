from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from locations.models import Location
from accounts.models import Player
from cards.models import CARD_IN_HAND, CARD_IN_PLAY, CARD_IN_DISCARD

@login_required (login_url='/accounts/login/')
def journal(request):
	player = get_object_or_404 (Player, user = request.user)

	return render (request, 'journal/index.html', {'logs' : player.log_set.order_by ('logged').all (), 'hand': [card.card for card in player.getCards (CARD_IN_HAND).all ()], 'request': request, 'numcardsindeck': player.deck.getNumCards (player)})
# Create your views here.

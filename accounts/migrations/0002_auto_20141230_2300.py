# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from accounts.models import Player
from cards.models import PLAYER_STATS, CARD_IN_DECK, PlayerCard, Deck, CardTemplate, StatTemplate

from django.contrib.auth.models import User

def makeAwesomePeople (apps, schema_editor):
    User = apps.get_model ('auth', 'User')
    db_alias = schema_editor.connection.alias
        
    User.objects.using (db_alias).bulk_create([
        User (date_joined = "2014-09-24T06:03:56.267Z", last_login = "2014-09-24T06:04:04.863Z", first_name = "Justin", last_name = "Brown", is_staff = True, username = "justinbrown", is_active = True, email = "brown.justin.michael@gmail.com", password = "pbkdf2_sha256$12000$JgAopSkAH1aN$jFKrm6ma6yVZ2+Ua1dImHOIXu6Ols/bdfUns7DpRJDI=", is_superuser = True),
        User (date_joined = "2014-09-23T04:29:44Z", last_login = "2014-09-23T04:29:44Z", first_name = "Nathan", last_name = "Brown", is_staff = True, username = "NathanBrown", is_active = True, email = "Brown.Nathan.Andrew@gmail.com", password = "pbkdf2_sha256$12000$RJubOgT7a0Kp$pq2n0N9+HUq49f80Bk75nky2NBlWX+lZAa00ixW+l+A=", is_superuser = True),
        User (date_joined = "2014-09-23T04:31:32Z", last_login = "2014-09-23T04:31:32Z", first_name = "Richard", last_name = "Thomas", is_staff = True, username = "RichardThomas", is_active = True, email = "Allattos@gmail.com", password = "pbkdf2_sha256$12000$BK8XF5EbsDeY$o7vwY2vNkNcc2JJEe/d0vwGXqpj2OFpwsaQrTea15Ow=", is_superuser = True),
    ])

def makePlayers (apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Card = PlayerCard
    Template = StatTemplate
    db_alias = schema_editor.connection.alias
    
    Player.objects.bulk_create ([
        Player (force = 3, dash = 2, resist = 2, charm = 1, user = user, deck = Deck.objects.create ()) for user in User.objects.all ()
    ])
    
    for player in Player.objects.all ():
        for stat in PLAYER_STATS:
            template = Template.objects.filter (stat = stat [0]).first ()
            for i in range (getattr (player, stat [0])):
                Card.objects.create (
                    modifier = i + 1, deck = player.deck, template = template
                )


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('accounts', '0001_initial'),
        ('locations', '0001_initial'),
        ('events', '0002_event_npc'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggerlog',
            name='trigger',
            field=models.ForeignKey(to='events.EventTrigger'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='active_event',
            field=models.ForeignKey(blank=True, null=True, to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='active_location',
            field=models.ForeignKey(blank=True, null=True, to='locations.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='deck',
            field=models.OneToOneField(blank=True, related_name='player', null=True, to='cards.Deck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='event',
            field=models.ForeignKey(blank=True, null=True, to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='location',
            field=models.ForeignKey(to='locations.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, related_name='polymorphic_accounts.log_set', null=True, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deckstatus',
            name='deck',
            field=models.ForeignKey(to='cards.Deck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deckstatus',
            name='location',
            field=models.ForeignKey(blank=True, null=True, to='locations.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deckstatus',
            name='player',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='deckstatus',
            unique_together=set([('player', 'deck')]),
        ),
        migrations.AddField(
            model_name='cardstatus',
            name='card',
            field=models.ForeignKey(to='cards.BaseCard'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardstatus',
            name='deck',
            field=models.ForeignKey(to='accounts.DeckStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardstatus',
            name='targetDeck',
            field=models.ForeignKey(blank=True, related_name='_unused_1', null=True, default=None, to='accounts.DeckStatus'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='cardstatus',
            unique_together=set([('deck', 'position', 'status')]),
        ),
        migrations.AddField(
            model_name='activeevent',
            name='cardStatus',
            field=models.ForeignKey(to='accounts.CardStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activeevent',
            name='event',
            field=models.ForeignKey(to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activeevent',
            name='player',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='activeevent',
            unique_together=set([('player', 'event', 'stackOrder')]),
        ),
        migrations.RunPython (makeAwesomePeople),
        migrations.RunPython (makePlayers),
    ]

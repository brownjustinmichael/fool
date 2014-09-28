from django.contrib import admin
from accounts.models import Player
from django.core.urlresolvers import reverse

class PlayerAdmin (admin.ModelAdmin):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            'script.js',       # project static folder
        )
    
admin.site.register(Player, PlayerAdmin)

from django.contrib import admin
from locations.models import Location, GlobalEventTrigger
from events.models import EventTrigger
from npcs.models import NPCLink
 
class NPCLinkInline(admin.TabularInline):
    model = NPCLink
    
class EventTriggerInline(admin.TabularInline):
    model = EventTrigger
    fk_name = "originalEvent"
    
class LocationAdmin (admin.ModelAdmin):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            'script.js',       # project static folder
        )
    inlines = [
        NPCLinkInline,
        EventTriggerInline,
    ]
 
admin.site.register (GlobalEventTrigger)
admin.site.register (Location, LocationAdmin)
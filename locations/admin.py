from django.contrib import admin
from locations.models import Location, LocationTrigger, GlobalEventTrigger
from npcs.models import NPCLink
 
class NPCLinkInline(admin.TabularInline):
    model = NPCLink
    
class LocationTriggerInline(admin.TabularInline):
    model = LocationTrigger
    
class LocationAdmin (admin.ModelAdmin):
    inlines = [
        NPCLinkInline,
        LocationTriggerInline,
    ]
 
admin.site.register (LocationTrigger)
admin.site.register (GlobalEventTrigger)
admin.site.register (Location, LocationAdmin)
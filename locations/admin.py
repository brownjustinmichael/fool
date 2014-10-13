from django.contrib import admin
from locations.models import Location, EventTrigger, GlobalEventTrigger
 
class EventTriggerInline(admin.TabularInline):
    model = EventTrigger
    
class LocationAdmin (admin.ModelAdmin):
    inlines = [
        EventTriggerInline,
    ]
 
admin.site.register (EventTrigger)
admin.site.register (GlobalEventTrigger)
admin.site.register (Location, LocationAdmin)
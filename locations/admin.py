from django.contrib import admin
from locations.models import Location, EventTrigger
 
class EventTriggerInline(admin.TabularInline):
    model = EventTrigger
    
class LocationAdmin (admin.ModelAdmin):
    inlines = [
        EventTriggerInline,
    ]
 
admin.site.register (EventTrigger)
admin.site.register(Location, LocationAdmin)
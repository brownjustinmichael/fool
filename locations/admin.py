from django.contrib import admin
from locations.models import Location, LocationTrigger, GlobalEventTrigger
 
class LocationTriggerInline(admin.TabularInline):
    model = LocationTrigger
    
class LocationAdmin (admin.ModelAdmin):
    inlines = [
        LocationTriggerInline,
    ]
 
admin.site.register (LocationTrigger)
admin.site.register (GlobalEventTrigger)
admin.site.register (Location, LocationAdmin)
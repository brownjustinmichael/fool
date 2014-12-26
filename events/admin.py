from django.contrib import admin
from events.models import Event, EventTrigger


class EventTriggerInline(admin.TabularInline):
    model = EventTrigger
    fk_name = "originalEvent"

class EventAdmin (admin.ModelAdmin):
    inlines = [
        EventTriggerInline,
    ]
 
admin.site.register (Event, EventAdmin)
admin.site.register (EventTrigger)

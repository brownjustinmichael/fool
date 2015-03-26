from django.contrib import admin
from events.models import Event, EventTrigger, EventEffect

class EventTriggerInline(admin.TabularInline):
    model = EventTrigger
    fk_name = "originalEvent"
    ordering = ['template', "threshold"]

class EffectInline(admin.TabularInline):
    model = EventEffect

class EventAdmin (admin.ModelAdmin):
    inlines = [
        EffectInline, EventTriggerInline,
    ]
 
admin.site.register (Event, EventAdmin)
admin.site.register (EventTrigger)


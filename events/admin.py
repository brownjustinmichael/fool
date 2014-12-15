from django.contrib import admin
from events.models import Event, ResultCondition, EventTrigger

class ResultConditionInline(admin.TabularInline):
    model = ResultCondition

class EventTriggerInline(admin.TabularInline):
    model = EventTrigger
    fk_name = "originalEvent"

class EventAdmin (admin.ModelAdmin):
    inlines = [
        EventTriggerInline,
        ResultConditionInline,
    ]
 
admin.site.register (Event, EventAdmin)
admin.site.register (EventTrigger)
admin.site.register (ResultCondition)

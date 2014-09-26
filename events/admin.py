from django.contrib import admin
from events.models import Event
from results.models import ResultCondition

class ResultConditionInline(admin.TabularInline):
    model = ResultCondition
    
class EventAdmin (admin.ModelAdmin):
    inlines = [
        ResultConditionInline,
    ]
 
admin.site.register (Event, EventAdmin)

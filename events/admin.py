from django.contrib import admin
from events.models import Event, ResultCondition

class ResultConditionInline(admin.TabularInline):
    model = ResultCondition
    
class EventAdmin (admin.ModelAdmin):
    inlines = [
        ResultConditionInline,
    ]
 
admin.site.register (Event, EventAdmin)
admin.site.register (ResultCondition)

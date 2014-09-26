from django.contrib import admin
from results.models import Result, ResultCondition, EnemyResult, StatResult, NewEventResult

admin.site.register (Result)
admin.site.register (EnemyResult)
admin.site.register (StatResult)
admin.site.register (NewEventResult)
admin.site.register (ResultCondition)

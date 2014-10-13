from django.contrib import admin
from results.models import Result, EnemyResult, StatResult, NewEventResult, NewCardResult

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

class ResultChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Result

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
        # ...
    # )

class StatResultAdmin(ResultChildAdmin):
    # define custom features here
    pass

class NewEventResultAdmin(ResultChildAdmin):
    # define custom features here
    pass
    
class NewCardResultAdmin(ResultChildAdmin):
    # define custom features here
    pass
    
class EnemyResultAdmin(ResultChildAdmin):
    # define custom features here
    pass

class ResultParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Result
    child_models = (
        (Result, ResultChildAdmin),
        (StatResult, StatResultAdmin),
        (NewEventResult, NewEventResultAdmin),
        (EnemyResult, EnemyResultAdmin),
        (NewCardResult, NewCardResultAdmin),
    )

# Only the parent needs to be registered:
admin.site.register(Result, ResultParentAdmin)

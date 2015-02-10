from django.contrib import admin
from accounts.models import Player, CardStatus, DeckStatus, Log, TriggerLog, ActiveEvent, PlayerFlag, Flag, LogFlag
from django.core.urlresolvers import reverse
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin


class CardStatusInline(admin.TabularInline):
    model = CardStatus
    fk_name = 'deck'
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(CardStatusInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if request._obj_ is not None:
            field.queryset = field.queryset.filter(deck__exact = request._obj_.deck)
        else:
            field.queryset = field.queryset.none()

        return field
        
class ActiveEventInline(admin.TabularInline):
    model = ActiveEvent

class DeckStatusInline(admin.TabularInline):
    model = DeckStatus
    
class DeckStatusAdmin (admin.ModelAdmin):
    inlines = [CardStatusInline]
    
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(DeckStatusAdmin, self).get_form(request, obj, **kwargs)
    
class PlayerFlagInline (admin.TabularInline):
    model = PlayerFlag

class PlayerAdmin (admin.ModelAdmin):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            'script.js',       # project static folder
        )
    inlines = [DeckStatusInline, ActiveEventInline, PlayerFlagInline]
    
admin.site.register(Player, PlayerAdmin)
admin.site.register(DeckStatus, DeckStatusAdmin)
admin.site.register (CardStatus)
admin.site.register (Flag)
# admin.site.register (Log)


class LogFlagInline (admin.TabularInline):
    model = LogFlag

class LogChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Log
    inlines = [LogFlagInline]

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
        # ...
    # )

class TriggerLogAdmin(LogChildAdmin):
    # define custom features here
    inlines = [LogFlagInline]
    
class LogParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Log
    child_models = (
        (Log, LogChildAdmin),
        (TriggerLog, TriggerLogAdmin),
    )

# Only the parent needs to be registered:
admin.site.register(Log, LogParentAdmin)

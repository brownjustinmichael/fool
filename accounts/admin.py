from django.contrib import admin
from accounts.models import Player, CardStatus, DeckStatus
from django.core.urlresolvers import reverse

class CardStatusInline(admin.TabularInline):
    model = CardStatus
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(CardStatusInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if request._obj_ is not None:
            field.queryset = field.queryset.filter(deck__exact = request._obj_)  
        else:
            field.queryset = field.queryset.none()

        return field

class DeckStatusInline(admin.TabularInline):
    model = DeckStatus
    
class DeckStatusAdmin (admin.ModelAdmin):
    inlines = [CardStatusInline]
    
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(DeckStatusAdmin, self).get_form(request, obj, **kwargs)
    

class PlayerAdmin (admin.ModelAdmin):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            'script.js',       # project static folder
        )
    inlines = [DeckStatusInline]
        
        
    
admin.site.register(Player, PlayerAdmin)
admin.site.register(DeckStatus, DeckStatusAdmin)
admin.site.register (CardStatus)

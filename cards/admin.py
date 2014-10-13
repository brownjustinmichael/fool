from django.contrib import admin
from cards.models import CardTemplate, StatTemplate, ItemTemplate, Card, PlayerCard, Deck

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

class CardInline(admin.TabularInline):
    model = Card

class DeckAdmin (admin.ModelAdmin):
    inlines = [
        CardInline,
    ]
    
class CardChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Card

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
        # ...
    # )

class PlayerCardAdmin(CardChildAdmin):
    # define custom features here
    pass

class CardParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Card
    child_models = (
        (Card, CardChildAdmin),
        (PlayerCard, PlayerCardAdmin),
    )
    
class CardTemplateChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = CardTemplate

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
        # ...
    # )

class StatTemplateAdmin(CardChildAdmin):
    # define custom features here
    pass
    
class ItemTemplateAdmin(CardChildAdmin):
    # define custom features here
    pass

class CardTemplateParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = CardTemplate
    child_models = (
        (StatTemplate, StatTemplateAdmin),
        (ItemTemplate, ItemTemplateAdmin),
    )
    
admin.site.register (Card, CardParentAdmin)
admin.site.register (Deck, DeckAdmin)
admin.site.register (CardTemplate, CardTemplateParentAdmin)

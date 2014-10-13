from django.contrib import admin
from cards.models import CardTemplate, StatTemplate, ItemTemplate, BaseCard, Card, PlayerCard, ItemCard, Deck, Effect, HealEffect

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

class CardInline(admin.TabularInline):
    model = Card
    # fk_name = 'card'
    readonly_fields = ['basecard_ptr']
    
class PlayerCardInline(admin.TabularInline):
    model = PlayerCard
    # fk_name = 'playercard'
    readonly_fields = ['basecard_ptr']

class ItemCardInline(admin.TabularInline):
    model = ItemCard
    # fk_name = 'itemcard'
    readonly_fields = ['basecard_ptr']

class DeckAdmin (admin.ModelAdmin):
    inlines = [
        CardInline,
        PlayerCardInline,
        ItemCardInline,
    ]
    
class BaseCardChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = BaseCard

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
        # ...
    # )

class CardAdmin(BaseCardChildAdmin):
    # define custom features here
    pass
    
class PlayerCardAdmin(BaseCardChildAdmin):
    # define custom features here
    pass
    
class ItemCardAdmin(BaseCardChildAdmin):
    # define custom features here
    pass

class BaseCardParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = BaseCard
    child_models = (
        # (BaseCard, BaseCardChildAdmin),
        (Card, CardAdmin),
        (PlayerCard, PlayerCardAdmin),
        (ItemCard, ItemCardAdmin),
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

class StatTemplateAdmin(CardTemplateChildAdmin):
    # define custom features here
    pass
    
class ItemTemplateAdmin(CardTemplateChildAdmin):
    # define custom features here
    pass

class CardTemplateParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = CardTemplate
    child_models = (
        (StatTemplate, StatTemplateAdmin),
        (ItemTemplate, ItemTemplateAdmin),
    )
    
class EffectChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Effect

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
        # ...
    # )

class HealEffectAdmin(EffectChildAdmin):
    # define custom features here
    pass

class EffectParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Effect
    child_models = (
        (HealEffect, HealEffectAdmin),
    )
    
admin.site.register (Effect, EffectParentAdmin)
admin.site.register (BaseCard, BaseCardParentAdmin)
admin.site.register (Deck, DeckAdmin)
admin.site.register (CardTemplate, CardTemplateParentAdmin)

from django.contrib import admin
from accounts.models import UserProfile
from cards.models import CardAttributes

class CardAttributesInline(admin.TabularInline):
    model = CardAttributes

class UserProfileAdmin (admin.ModelAdmin):
    inlines = [
        CardAttributesInline,
    ]

admin.site.register(UserProfile, UserProfileAdmin)

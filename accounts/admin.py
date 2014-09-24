from django.contrib import admin
from accounts.models import UserProfile
from cards.models import CardAttribute

class CardAttributeInline(admin.TabularInline):
    model = CardAttribute

class UserProfileAdmin (admin.ModelAdmin):
    inlines = [
        CardAttributeInline,
    ]

admin.site.register(UserProfile, UserProfileAdmin)

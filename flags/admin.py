from django.contrib import admin
from flags.models import Flag, FlagDependency

class FlagDependencyInline(admin.TabularInline):
    model = FlagDependency
    fk_name = 'dependent_flag'
    
class FlagAdmin (admin.ModelAdmin):
    inlines = [FlagDependencyInline]
    
admin.site.register (Flag, FlagAdmin)

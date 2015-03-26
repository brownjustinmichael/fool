from django.contrib import admin
from flags.models import nFlag, nFlagDependency

class nFlagDependencyInline(admin.TabularInline):
    model = nFlagDependency
    fk_name = 'dependent_flag'
    
class nFlagAdmin (admin.ModelAdmin):
    inlines = [nFlagDependencyInline]
    
admin.site.register (nFlag, nFlagAdmin)

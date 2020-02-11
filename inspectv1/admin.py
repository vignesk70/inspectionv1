from django.contrib import admin
from .models import *
admin.AdminSite.site_header='Inspect'
# Register your models here.

class CategoryItemInline(admin.TabularInline):
    model = ItemInCategory
    extras = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    inlines = [CategoryItemInline]
    save_as = True


#admin.site.register(InspectionCategory)
#admin.site.register(ItemInCategory)
admin.site.register(Sites)
admin.site.register(InspectionCategory,CategoryAdmin)
admin.site.register(Shyam)
admin.site.register(InspectionDetails)
#admin.site.register(ItemInCategory)

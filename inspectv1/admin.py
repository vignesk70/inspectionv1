from django.contrib import admin
from .models import *
admin.AdminSite.site_header='Inspect'
# Register your models here.

class CategoryItemInline(admin.TabularInline):
    model = ItemInCategory
    extra = 0



'''class InspectedInline(admin.TabularInline):
    model = Inspected_Item
    extras = 1'''

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    inlines = [CategoryItemInline]
    save_as = True

class InspectItemAdmin(admin.ModelAdmin):
    #list_display = ('Cat',)
    list_display=('category_name','site_name','inspector_name','Items','image')
    #inlines = [InspectedInline]
    save_as = True
    def has_add_permission(self, request, obj=None):
        return False

    '''def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False'''


class InspectedItemAdmin(admin.ModelAdmin):
    list_display = ('site_id', 'item_value', 'add_date', 'update_date', 'category_id', 'user_id')
    list_filter = ('category_id', 'user_id')
    #fields = ['category_id', 'site_id', 'user_id', ('date_of_birth', 'date_of_death')]



#admin.site.register(InspectItem, InspectItemAdmin)




#admin.site.register(InspectionCategory)
#admin.site.register(ItemInCategory)
admin.site.register(Sites)
admin.site.register(InspectionCategory,CategoryAdmin)
admin.site.register(InspectedItem, InspectedItemAdmin)
#admin.site.register(Inspected_Item)
admin.site.register(InspectorDetails)
#admin.site.register(ItemInCategory)
admin.site.register(Subsidiary)
admin.site.register(Stoffice)


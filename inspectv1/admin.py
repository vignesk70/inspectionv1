from django.contrib import admin
from .models import *
admin.AdminSite.site_header='Inspect'
# Register your models here.

class CategoryItemInline(admin.TabularInline):
    model = ItemInCategory
    extras = 1

'''class InspectedInline(admin.TabularInline):
    model = Inspected_Item
    extras = 1'''

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    inlines = [CategoryItemInline]
    save_as = True

class Inspect_ItemAdmin(admin.ModelAdmin):
    #list_display = ('Cat',)
    list_display=('Site_id','Inspect_id','Item_id','fieldname')
    #inlines = [InspectedInline]
    save_as = True
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Inspect_Item, Inspect_ItemAdmin)



#admin.site.register(InspectionCategory)
#admin.site.register(ItemInCategory)
admin.site.register(Sites)
admin.site.register(InspectionCategory,CategoryAdmin)
#admin.site.register(Inspected_Item)
admin.site.register(InspectionDetails)
#admin.site.register(ItemInCategory)
admin.site.register(sub)
admin.site.register(stoffice)
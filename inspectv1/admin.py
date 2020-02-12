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

class Inspected_ItemAdmin(admin.ModelAdmin):
    #list_display = ('Cat',)
    list_display=('S_id','Ins_id','item_id','field_value')
    #inlines = [InspectedInline]
    save_as = True


admin.site.register(Inspected_Item, Inspected_ItemAdmin)



#admin.site.register(InspectionCategory)
#admin.site.register(ItemInCategory)
admin.site.register(Sites)
admin.site.register(InspectionCategory,CategoryAdmin)
#admin.site.register(Inspected_Item)
admin.site.register(InspectionDetails)
#admin.site.register(ItemInCategory)

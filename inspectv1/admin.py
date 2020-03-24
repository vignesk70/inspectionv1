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


class InspectedItemInline(admin.TabularInline):
    model = InspectedItem
    extra = 0


class InspectedItemAdmin(admin.ModelAdmin):
    view_on_site = True
   
    list_display = (
        # put all other fields you want to be shown in listing
        'category_name',
    )
    def category_name(self, obj):
        return obj.category 


    def get_absolute_url(self):
        return "/people/%i/" % self.id   


    def changelist_view(self, request, *args, **kwargs):
        self.request = request
        return super().changelist_view(request, *args, **kwargs)

    def change(self, obj):
        request = getattr(self, 'request', None)
        if request:
            return "/people/%i/" % self.id     
           # use request.GET to construct the link   
   


    #list_display = ('site_id', 'item_value', 'add_date', 'update_date', 'category_id', 'user_id')
    #list_filter = ('category_id', 'user_id')

    """def changelist_view(self, request, extra_context=None):
        # Add extra context data to pass to change list template
        extra_context = extra_context or {}
        extra_context['my_store_data'] = {'onsale':['Item 1','Item 2']}
        # Execute default logic from parent class changelist_view()
        return super(StoreAdmin, self).changelist_view(
            request, extra_context=extra_context
        )"""

    #list_select_related = (
    #   'category_id', 'user_id',
    #)
    change_list_template = 'admin/inspecteditemlist.html'

    def get_queryset(self, request):
        context_object_name = 'category'
        my_param = request.GET.get('q')
        #if request.GET.q == "":
        if my_param is None:
            return InspectionCategory.objects.all()



    

        #context_object_name = 'inspecteditem'
        #return InspectedItem.objects.all()
    
    #inlines = [InspectedItemInline]
    #save_as = True

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


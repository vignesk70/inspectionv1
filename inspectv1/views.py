from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from django.contrib import messages


# Create your views here.
class IndexView(TemplateView):
    template_name = "inspectv1/index.html"

    
class ShowInspectionData(ListView):
    template_name = "inspectv1/updateinspection.html"
   # model=ItemInCategory

    #fields = ['category','items']
    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()
    
'''def Add(request):
    print("In Add")
    if request.method == 'POST':
        print("In Add")
    
        
        field_name1 = 'sequence'
        field_name2='id'
        obj =InspectionCategory.objects.first()
        field_object = InspectionCategory._meta.get_field(field_name1)
        field_value1 = field_object.value_from_object(obj)

        obj2 =InspectionDetails.objects.first()
        field_object = InspectionDetails._meta.get_field(field_name2)
        field_value2 = field_object.value_from_object(obj2)

        obj2 =InspectionCategory.objects.first()
        field_object = InspectionCategory._meta.get_field(field_name2)
        field_value3 = field_object.value_from_object(obj2)

        obj2 =ItemInCategory.objects.first()
        field_object = ItemInCategory._meta.get_field(field_name2)
        field_value4 = field_object.value_from_object(obj2)
        if  request.POST.get('option') or request.POST.get('status'):
            print("Come Inside")
            shyam=Inspect_Item()
            
            #shyam.field_value=request.POST.get('status')
            shyam.Site_id=field_value1
            shyam.Inspect_id=field_value2
            shyam.Cat_id=field_value4
            shyam.Item_id=field_value3
            

            shyam.Items= request.POST.get('field')
            shyam.fieldname=request.POST.get('status')
            #shyam.status= request.POST.get('option')
            shyam.image= request.POST.get('my_image')
            shyam.save()
            messages.success(request, 'Changes successfully saved.')
            return HttpResponseRedirect('/inspect/inspection')

        else:
            return HttpResponse("NotDone")
'''            

def Add(request):
    print("In Add")
    if request.method == 'POST':
        print("In Add") 

        field_name1 = 'category'
        field_name2='name'
        field_name3='users'
        field_name4='items'
        field_name5='id'
        obj =InspectionCategory.objects.first()
        field_object = InspectionCategory._meta.get_field(field_name1)
        field_value1 = field_object.value_from_object(obj)

        obj2 =InspectionDetails.objects.first()
        field_object = InspectionDetails._meta.get_field(field_name3)
        field_value2 = field_object.value_from_object(obj2)

        obj2 =Sites.objects.first()
        field_object = Sites._meta.get_field(field_name2)
        field_value3 = field_object.value_from_object(obj2)

        obj2 =ItemInCategory.objects.first()
        field_object = ItemInCategory._meta.get_field(field_name4)
        field_value4 = field_object.value_from_object(obj2)

        obj2 =ItemInCategory.objects.first()
        field_object = ItemInCategory._meta.get_field(field_name5)
        field_value5 = field_object.value_from_object(obj2)
        print(request.POST['field'])
        print(request.POST['status'])
        print(request.POST['my_image'])
        if  request.POST.get('field') or request.POST.get('status'):
            print("Come Inside")
            #print(request.POST.get('my_image'))
            shyam=Inspect_Item()
            
            #shyam.field_value=request.POST.get('status')
            shyam.site_name=field_value3


            shyam.Inspector_Name=field_value2
            shyam.category_name=field_value1
            shyam.Item_id=field_value5
            

            shyam.Items= request.POST['field']
            shyam.fieldname=request.POST['status']
            #shyam.status= request.POST.get('option')
            shyam.image= request.POST['my_image']
            shyam.save()
            messages.success(request, 'Category Add Successfully.')
            return HttpResponseRedirect('/inspect/inspection')

        else:
            return HttpResponse("NotDone")   
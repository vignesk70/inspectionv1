from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from .models import *
from django.http import HttpResponse
from .forms import *

# Create your views here.
class IndexView(TemplateView):
    template_name = "inspectv1/index.html"

    
class ShowInspectionData(ListView):
    template_name = "inspectv1/updateinspection.html"
   # model=ItemInCategory

    #fields = ['category','items']
    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()
    
def Add(request):
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
            shyam.S_id=field_value1
            shyam.Ins_id=field_value2
            shyam.Cat_id=field_value4
            shyam.item_id=field_value3
            print(request.POST.get('my_image'))

            shyam.items= request.POST.get('field')
            shyam.field_value=request.POST.get('status')
            shyam.status= request.POST.get('option')
            shyam.image= request.POST.get('my_image')
            shyam.save()
            return redirect('inspectv1:updateinspection.html')

        else:
            return HttpResponse("NotDone")

            

        
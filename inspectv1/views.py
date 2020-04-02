import os
import json

from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django import forms
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from .forms import InspectionData
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from .models import ItemInCategory




# Create your views here.
class IndexView(TemplateView):
    template_name = "inspectv1/index.html"


class CreateInspectionForm(CreateView):
    template_name = "inspectv1/inspection.html"
    form_class =  RunInspection


class ShowInspectionData(FormMixin, ListView):
    template_name = "inspectv1/updateinspection.html"
    form_class = InspectionData

    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()

    
"""class ShowInspectionDataText(ListView):
    template_name = "inspectv1/updateinspectiontest.html"
    model = Profile
    form_class=ProfileForm
    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()

    def get_object(self):
        return InspectionCategory.objects.all() 

    def get(self, request, *args, **kwargs):
        #self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #car_form = CarRegistrationFormSet()
        #receipt_form = PaymentFormSet()
        return self.render_to_response(
            self.get_context_data(form=form)) """



def GetCategories(request):
    print("In Add")


def Add(request):
    print("In Add")
    #return HttpResponse(request.POST['category_id']) 

    if request.method == 'POST':
        current_user = request.user

        image = request.FILES['item_image']
        image_types = [
            'image/png', 'image/jpg',
            'image/jpeg', 'image/pjpeg', 'image/gif'
        ]
        if image.content_type not in image_types:
            data = json.dumps({
                'status': 405,
                'error': _('Bad image format.')
            })
            return HttpResponse(
                data, content_type="application/json", status=405)

        tmp_file = os.path.join(settings.MEDIA_ROOT, image.name)
        path = default_storage.save(tmp_file, ContentFile(image.read()))
        img_url = os.path.join(settings.MEDIA_URL, path)

        return HttpResponse(request.POST.items())
        #print current_user.id
        #return HttpResponse(request.FILES)
        inspectObj = InspectedItem()

        inspectObj.category_id_id = request.POST['category_id']
        inspectObj.site_id_id = request.POST['site_id']
        inspectObj.user_id_id = current_user.id
        inspectObj.item_id_id = request.POST['item_id']
        inspectObj.item_value = request.POST['item_value']
        #inspectObj.item_image = 1
        inspectObj.save()

        return HttpResponse(request.POST.items())

    else:
        return HttpResponse("0")  

    """if request.method == 'POST':
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
            shyam=InspectItem()
            
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
            return HttpResponse("NotDone")  """ 
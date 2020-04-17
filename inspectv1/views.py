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
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt


from .models import ItemInCategory




# Create your views here.
class IndexView(TemplateView):
    template_name = "inspectv1/index.html"


class CreateInspectionForm(CreateView):
    template_name = "inspectv1/inspection.html"
    form_class =  RunInspection


class ShowInspectionData(ListView):
    template_name = "inspectv1/updateinspection.html"
    #form_class = InspectionData

    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()

    def get_submit_status(self):
        return "testtest"

    """def get_queryset(self):
        qs1 = InspectionCategory.objects.all() #your first qs
        qs2 = InspectedItem.objects.all()  #your second qs
        #you can add as many qs as you want
        queryset = sorted(chain(qs1,qs2))
        return queryset"""

    
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

class ShowSiteData(ListView):
    template_name = "inspectv1/sites.html"
    #form_class = InspectionData

    context_object_name = 'sites'
    queryset = Sites.objects.all()

    #def get_queryset(self):
        #user_id = self.request.user.id
        #return Sites.objects.all().filter(user_id_id=user_id).select_related()

    #def get_context_data(self, **kwargs):
        #context =  super(SCcheckDetailView, self).get_context_data(**kwargs)
        #context['car'] = Car.objects.get(pk=self.kwargs.get('pk',None))
        #context['member'] = Member.objects.get(id=context['car'].member_id.pk)
        #context_object_name = 'sites'
        #user_id = self.get_user();
        #queryset = Sites.objects.all().filter(user_id_id=user_id).select_related()
        #return context

def ShowInspectionDataFun(request):

    category = InspectionCategory.objects.all().select_related()

    my_param = request.GET.get('site')
    if my_param is None:
        return render(request, 'inspectv1/updateinspection.html', {'category': category})


    sites = Sites.objects.filter(site_no=request.GET['site'])

    for site in sites:
        siteid = site.id

    posts = InspectedItem.objects.all().filter(user_id_id=request.user.id, site_id_id = siteid ).select_related()


    
    for cat in category:
        for post in posts:
            if cat.id == post.category_id_id:
                cat.filled = 1
            else:
                cat.filled = 0

        """items = cat.items.all
        for list in items:
            for post in posts:
                if(post.item_id_id == list.id ):
                   list.filledvalue =  post.item_value"""

    return render(request, 'inspectv1/updateinspection.html', {'category': category, 'posts': posts})


@csrf_exempt
def GetCategories(request):
    if request.method == 'POST':
        sites = Sites.objects.all().filter(site_no=request.POST['siteid'])
        site_count = Sites.objects.all().filter(site_no=request.POST['siteid']).count()

        if site_count ==0:
            return HttpResponse(site_count)
        else:
            html = render_to_string('inspectv1/createsite.html', {'sites': sites})
            return HttpResponse(html)
    else:
        return HttpResponse(0)

@csrf_exempt
def Add(request):
    print("In Add")
    #return HttpResponse(request.POST['category_id']) 

    if request.method == 'POST':
        current_user = request.user

        """image = request.FILES['item_image']
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

        return HttpResponse(request.POST.items())"""
        #print current_user.id
        #return HttpResponse(request.FILES)
        sites = Sites.objects.filter(site_no=request.POST['site_id'])

        for site in sites:
            siteid = site.id

        

        inspectObj = InspectedItem()

        inspectObj.category_id_id = request.POST['category_id']
        inspectObj.site_id_id = siteid
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
import os
import json
import array as arr

from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView
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
from django.contrib.auth.decorators import login_required



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
@login_required
def ShowInspectionDataFun(request):

    category = InspectionCategory.objects.all().select_related()

    my_param = request.GET.get('site')
    if my_param is None:
        return render(request, 'inspectv1/updateinspection.html', {'category': category})


    sites = Sites.objects.filter(site_no=request.GET['site'])

    for site in sites:
        siteid = site.id

    inspectionmaster = InspectionMaster.objects.all().filter(user_id_id=request.user.id, site_id_id = siteid ).select_related()
    master_id = 0

    for im in inspectionmaster:
        master_id = im.id

   
    if master_id == "0":
        return render(request, 'inspectv1/updateinspection.html', {'category': category})

    #posts = InspectedItem.objects.all().filter(user_id_id=request.user.id, site_id_id = siteid ).select_related()
    posts = InspectionDetails.objects.all().filter(master_id_id = master_id ).select_related()


    
    for cat in category:
        for post in posts:
            if cat.id == post.category_id_id:
                cat.filled = 1
            

        for list in cat.items.all():
            if list.fieldtype == 'checkbox':
                for post in posts:
                    if post.item_id_id == list.id:
                        #if post.item_image:
                        cat.iserror = 1
                        #else:
                        #    cat.iserror = 1


    return render(request, 'inspectv1/updateinspection.html', {'category': category, 'posts': posts})


@login_required
def ShowSiteData(request):
   

    


    sites = Sites.objects.all()
    for site in sites:

        inspectionmaster = InspectionMaster.objects.all().filter(user_id_id=request.user.id, site_id_id = site.id ).select_related()
        master_id = 0
        for im in inspectionmaster:
            master_id = im.id
        
        site.master_id = master_id
        item_safety = ItemInCategory.objects.filter(errortype="SAFETY").values_list('id', flat=True)
        site.item_safety = InspectionDetails.objects.distinct("item_id_id").all().filter(master_id_id = master_id,  item_id_id__in=item_safety ).select_related().count()

        item_statutory = ItemInCategory.objects.filter(errortype="STATUTORY").values_list('id', flat=True)
        site.item_statutory = InspectionDetails.objects.distinct("item_id_id").all().filter(master_id_id = master_id, item_id_id__in=item_statutory ).select_related().count()

        item_engineering = ItemInCategory.objects.filter(errortype="ENGINEERING").values_list('id', flat=True)
        site.item_engineering = InspectionDetails.objects.distinct("item_id_id").all().filter(master_id_id = master_id, item_id_id__in=item_engineering ).select_related().count()

         

        item_operations = ItemInCategory.objects.filter(errortype="OPERATIONS").values_list('id', flat=True)
        site.item_operations = InspectionDetails.objects.distinct("item_id_id").all().filter(master_id_id = master_id, item_id_id__in=item_operations ).select_related().count()
        
        show_site = 0;
        if site.item_safety != 0:
            show_site = 1
        elif site.item_statutory != 0:
            show_site = 1
        elif site.item_engineering != 0:
            show_site = 1
        elif site.item_operations != 0:
            show_site = 1

        site.show_site = show_site



        #items = InspectedItem.objects.distinct("item_id_id").all().filter(user_id_id=request.user.id, site_id_id = site.id ).select_related()
        #filleditems = 0
        #for item in items:
        #    filleditems += 1

        #site.filleditems = filleditems;


    return render(request, 'inspectv1/sites.html', {'sites': sites, })

@csrf_exempt
def GetCategories(request):
    if request.method == 'POST':
        sites = Sites.objects.all().filter(site_no=request.POST['siteid'])
        site_count = Sites.objects.all().filter(site_no=request.POST['siteid']).count()
        category = InspectionCategory.objects.all()

        if site_count ==0:
            return HttpResponse(site_count)
        else:
            html = render_to_string('inspectv1/createsite.html', {'sites': request.POST['siteid'], 'category': category})
            return HttpResponse(html)
    else:
        return HttpResponse(0)

@csrf_exempt
def GetSites(request):
    if request.method == 'POST':
        

        if request.POST.get('siteid',False):        
            sites = Sites.objects.all().filter(site_no__contains=request.POST['siteid'])
            totalsites = Sites.objects.all().filter(site_no__contains=request.POST['siteid']).count() 
        elif request.POST.get('sitename',False): 
            sites = Sites.objects.all().filter(name__contains=request.POST['sitename'])
            totalsites = Sites.objects.all().filter(name__contains=request.POST['sitename']).count()


        #a_dict = dict()
        a_dict = [None] * totalsites
        
        countarr = 0
        for site in sites:
            sitevalue = str(site.site_no) + '-' + str(site.name)
            #a_dict.append(sitevalue)
            b_dict = [None] * 3
            b_dict[0] = site.site_no
            b_dict[1] = site.name
            b_dict[2] = sitevalue
            a_dict[countarr] = b_dict
            #a_dict[1] = sitevalue
            countarr += 1

        return HttpResponse(json.dumps(a_dict))
        

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

        
        if request.POST['master_id'] == '':  

            inspectObj = InspectionMaster()

            inspectObj.site_id_id = siteid
            inspectObj.user_id_id = current_user.id

            inspectObj.save()

            master_id = inspectObj.id
        else:
            master_id = request.POST['master_id']


        inspectDetailObj = InspectionDetails()

        inspectDetailObj.master_id_id = master_id
        inspectDetailObj.category_id_id = request.POST['category_id']
        inspectDetailObj.item_id_id = request.POST['item_id']
        inspectDetailObj.item_value = request.POST['item_value']
        if bool(request.FILES.get('item_image', False)) == True:
            inspectDetailObj.item_image = request.FILES['item_image']
        inspectDetailObj.save()

        return HttpResponse(master_id)

    else:
        return HttpResponse("0")  



        """inspectObj = InspectedItem()

        inspectObj.category_id_id = request.POST['category_id']
        inspectObj.site_id_id = siteid
        inspectObj.user_id_id = current_user.id
        inspectObj.item_id_id = request.POST['item_id']
        inspectObj.item_value = request.POST['item_value']
        if bool(request.FILES.get('item_image', False)) == True:
            inspectObj.item_image = request.FILES['item_image']
        inspectObj.save()

        return HttpResponse(request.POST.items())

    else:
        return HttpResponse("0")  """

    
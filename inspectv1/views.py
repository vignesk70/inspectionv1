import os
import json
import array as arr
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView
from django import forms
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404
from math import radians, acos, sin, cos
from django.db.models import Max, Min, Avg
from django.urls import reverse_lazy
from django.db.models import Count
from django.conf import settings
import dateutil.relativedelta as delta


# Create your views here.


class IndexView(TemplateView):
    template_name = "inspectv1/index.html"


class CreateInspectionForm(CreateView):
    template_name = "inspectv1/inspection.html"
    form_class = RunInspection


class ShowInspectionData(ListView):
    template_name = "inspectv1/updateinspection.html"
    # form_class = InspectionData

    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()

    def get_submit_status(self):
        return "testtest"

    """def get_queryset(self):
        qs1 = InspectionCategory.objects.all() #your first qs
        qs2 = InspectedItem.objects.all()  #your second qs
        # you can add as many qs as you want
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
        # self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # car_form = CarRegistrationFormSet()
        # receipt_form = PaymentFormSet()
        return self.render_to_response(
            self.get_context_data(form=form)) """
# def get_queryset(self):
# user_id = self.request.user.id
# return Sites.objects.all().filter(user_id_id=user_id).select_related()

# def get_context_data(self, **kwargs):
# context =  super(SCcheckDetailView, self).get_context_data(**kwargs)
# context['car'] = Car.objects.get(pk=self.kwargs.get('pk',None))
# context['member'] = Member.objects.get(id=context['car'].member_id.pk)
# context_object_name = 'sites'
# user_id = self.get_user();
# queryset = Sites.objects.all().filter(user_id_id=user_id).select_related()
# return context


@login_required
def ShowInspectionDataFun(request):

    category = InspectionCategory.objects.all().select_related()

    my_param = request.GET.get('site')
    if my_param is None:
        return render(request, 'inspectv1/updateinspection.html', {'category': category})

    # sites = Sites.objects.filter(site_no=request.GET['site'])
    sites = get_list_or_404(Sites, site_no=request.GET['site'])

    for site in sites:
        siteid = site.id
        sitename = site.name

    inspectionmaster = InspectionMaster.objects.all().filter(
        user_id_id=request.user.id, site_id_id=siteid).select_related()
    master_id = 0

    for im in inspectionmaster:
        master_id = im.id

    if master_id == "0":
        return render(request, 'inspectv1/updateinspection.html', {'category': category, 'site_data': sites})

    # posts = InspectedItem.objects.all().filter(user_id_id=request.user.id, site_id_id = siteid ).select_related()
    posts = InspectionDetails.objects.all().filter(
        master_id_id=master_id).select_related()

    for cat in category:
        for post in posts:
            if cat.id == post.category_id_id:
                cat.filled = 1

        for list in cat.items.all():
            # if list.fieldtype == 'checkbox':
            for post in posts:
                if post.item_id_id == list.id:
                    # if post.item_image:
                    if list.throw_error:
                        cat.iserror = 1
                    # else:
                    #    cat.iserror = 1

    return render(request, 'inspectv1/updateinspection.html', {'category': category, 'posts': posts, 'site_data': sites})


@login_required
def ShowSiteData(request):

    sites = Sites.objects.all()
    for site in sites:

        inspectionmaster = InspectionMaster.objects.all().filter(
            user_id_id=request.user.id, site_id_id=site.id).select_related()
        master_id = 0
        for im in inspectionmaster:
            master_id = im.id

        site.master_id = master_id
        item_safety = ItemInCategory.objects.filter(
            errortype="SAFETY").values_list('id', flat=True)
        site.item_safety = InspectionDetails.objects.distinct("item_id_id").all().filter(
            master_id_id=master_id,  item_id_id__in=item_safety).select_related().count()

        item_statutory = ItemInCategory.objects.filter(
            errortype="STATUTORY").values_list('id', flat=True)
        site.item_statutory = InspectionDetails.objects.distinct("item_id_id").all().filter(
            master_id_id=master_id, item_id_id__in=item_statutory).select_related().count()

        item_engineering = ItemInCategory.objects.filter(
            errortype="ENGINEERING").values_list('id', flat=True)
        site.item_engineering = InspectionDetails.objects.distinct("item_id_id").all().filter(
            master_id_id=master_id, item_id_id__in=item_engineering).select_related().count()

        item_operations = ItemInCategory.objects.filter(
            errortype="OPERATIONS").values_list('id', flat=True)
        site.item_operations = InspectionDetails.objects.distinct("item_id_id").all().filter(
            master_id_id=master_id, item_id_id__in=item_operations).select_related().count()

        show_site = 0
        if site.item_safety != 0:
            show_site = 1
        elif site.item_statutory != 0:
            show_site = 1
        elif site.item_engineering != 0:
            show_site = 1
        elif site.item_operations != 0:
            show_site = 1

        site.show_site = show_site

        # items = InspectedItem.objects.distinct("item_id_id").all().filter(user_id_id=request.user.id, site_id_id = site.id ).select_related()
        # filleditems = 0
        # for item in items:
        #    filleditems += 1

        # site.filleditems = filleditems;

    return render(request, 'inspectv1/sites.html', {'sites': sites, })


@csrf_exempt
def GetCategories(request):
    if request.method == 'POST':
        sites = Sites.objects.all().filter(site_no=request.POST['siteid'])
        site_count = Sites.objects.all().filter(
            site_no=request.POST['siteid']).count()
        category = InspectionCategory.objects.all()

        if site_count == 0:
            return HttpResponse(site_count)
        else:
            html = render_to_string(
                'inspectv1/createsite.html', {'sites': request.POST['siteid'], 'category': category})
            return HttpResponse(html)
    else:
        return HttpResponse(0)


@csrf_exempt
def GetSites(request):
    if request.method == 'POST':

        if request.POST.get('siteid', False):
            sites = Sites.objects.all().filter(
                site_no__contains=request.POST['siteid']).order_by('site_no')
            totalsites = Sites.objects.all().filter(
                site_no__contains=request.POST['siteid']).count()
        elif request.POST.get('sitename', False):
            sites = Sites.objects.all().filter(name__contains=str(
                request.POST['sitename']).upper()).order_by('name')
            totalsites = Sites.objects.all().filter(
                name__contains=str(request.POST['sitename']).upper()).count()

        # a_dict = dict()
        a_dict = [None] * totalsites

        countarr = 0
        for site in sites:
            sitevalue = str(site.site_no) + '-' + str(site.name)
            # a_dict.append(sitevalue)
            b_dict = [None] * 3
            b_dict[0] = site.site_no
            b_dict[1] = site.name
            b_dict[2] = sitevalue
            a_dict[countarr] = b_dict
            # a_dict[1] = sitevalue
            countarr += 1

        return HttpResponse(json.dumps(a_dict))


@csrf_exempt
def Add(request):
    if settings.DEBUG:
        print("In Add")

    # return HttpResponse(request.POST['category_id'])

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
        # print current_user.id
        # return HttpResponse(request.FILES)
        sites = Sites.objects.get(site_no=request.POST['site_id'])
        siteid = sites.id
        # for site in sites:
        #     siteid = site.id
        if settings.DEBUG:
            print("DEBUG:Siteid", siteid)
        master_id = 0
        # if 'dateadd' in request.POST:
        #     dateadd = request.POST['dateadd']
        #     # inspectionmaster = InspectionMaster.objects.all().filter(
        #     #     user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd).select_related()
        #     inspectionmaster = InspectionMaster.objects.get_or_create(
        #         user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
        # else:
        #     dateadd = None
        #     # inspectionmaster = InspectionMaster.objects.all().filter(
        #     # user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd).select_related()
        #     inspectionmaster = InspectionMaster.objects.get_or_create(
        #         user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
        # # for im in inspectionmaster:
        # #     master_id = im.id
        # master_id = inspectionmaster[0].id
        if settings.DEBUG:
            print("DEBUG:masterid", master_id)
        # if 'dateadd' in request.POST:
        #     dateadd = request.POST['dateadd']
        #     # inspectionmaster = InspectionMaster.objects.all().filter(
        #     #     user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd).select_related()
        #     inspectionmaster = InspectionMaster.objects.get_or_create(
        #         user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
        #     master_id = inspectionmaster[0].id
        if request.POST['master_id'] == '':
            # master_id = 0
            if 'dateadd' in request.POST:
                dateadd = request.POST['dateadd']
            # inspectionmaster = InspectionMaster.objects.all().filter(
            #     user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd).select_related()
                inspectionmaster = InspectionMaster.objects.filter(
                    user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
                # master_id = inspectionmaster[0].id
                if inspectionmaster:
                    for im in inspectionmaster:
                        master_id = im.id
                if settings.DEBUG:
                    print("DEBUG:masterid in dateadd", master_id)
            if master_id == 0:
                try:
                    inspectObj = InspectionMaster()
                    inspectObj.site_id_id = siteid
                    inspectObj.user_id_id = current_user.id
                    inspectObj.save()
                    master_id = inspectObj.id
                except Exception as err:
                    inspectionmaster = InspectionMaster.objects.filter(
                        user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
                # master_id = inspectionmaster[0].id
                    if inspectionmaster:
                        for im in inspectionmaster:
                            master_id = im.id
                    if settings.DEBUG:
                        print("Integrity Error", err)

        else:
            master_id = request.POST['master_id']
        if settings.DEBUG:
            print("DEBUG:masterid after save", master_id)
        inspectDetailObj = InspectionDetails()
        try:
            inspectDetailObj = InspectionDetails.objects.get(
                master_id_id=master_id, category_id_id=request.POST['category_id'], item_id_id=request.POST['item_id'])
            inspectDetailObj.item_value = request.POST['item_value']
            if bool(request.FILES.get('item_image', False)) == True:
                inspectDetailObj.item_image = request.FILES['item_image']
            inspectDetailObj.save()
        except InspectionDetails.DoesNotExist:
            inspectDetailObj.master_id_id = master_id
            inspectDetailObj.category_id_id = request.POST['category_id']
            inspectDetailObj.item_id_id = request.POST['item_id']
            inspectDetailObj.item_value = request.POST['item_value']
            if bool(request.FILES.get('item_image', False)) == True:
                inspectDetailObj.item_image = request.FILES['item_image']
            inspectDetailObj.save()
        # inspectDetailObj.master_id_id = master_id
        # inspectDetailObj.category_id_id = request.POST['category_id']
        # inspectDetailObj.item_id_id = request.POST['item_id']
        # inspectDetailObj.item_value = request.POST['item_value']
        # if bool(request.FILES.get('item_image', False)) == True:
        #     inspectDetailObj.item_image = request.FILES['item_image']
        # inspectDetailObj.save()

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


class ListSitesForInspector(LoginRequiredMixin, ListView):
    model = InspectionMaster
    template_name = 'inspectv1/listsites.html'
    form_class = DashboardDateFilterForm
    startdate = None
    enddate = None

    def get_context_data(self, **kwargs):
        sitedata = []
        context = super(ListSitesForInspector, self).get_context_data(**kwargs)
        try:
            if self.request.GET['start_date']:
                self.startdate = (self.request.GET['start_date'])
                self.enddate = (self.request.GET['end_date'])
                initial_dict = {'start_date': self.startdate,
                                'end_date': self.enddate}
                form = DashboardDateFilterForm(None, initial=initial_dict)
                context['form'] = form

        except:
            initial_dict = {'start_date': getstartq(self)[0].strftime("%Y-%m-%d"),
                            'end_date': datetime.now().strftime("%Y-%m-%d")}
            form = DashboardDateFilterForm(None, initial=initial_dict)
            context['form'] = form

        listofsites = InspectionMaster.objects.filter(
            user_id=self.request.user.id, add_date__range=getstartq(self)).order_by('-id')
        sitevisited = listofsites.count()
        for sites in listofsites:
            data = {}
            error = {}
            data['sitename'] = sites.site_id.name
            data['siteadd'] = sites.add_date
            data['siteid'] = sites.id
            data['siteno'] = sites.site_id.site_no
            for errors in getERRTYPE():
                error[errors] = getCount(sites.id, errors)

            sitedata.append(data)
            data["errors"] = error
        context['sitevisited'] = sitevisited
        context['headers'] = getERRTYPE()
        context["sitedata"] = sitedata

        # context["details"] = InspectionDetails.objects.all().filter()

        return context


def getERRTYPE():
    '''
    Get the list of errorTyples as part of the model for error categories.
    '''
    list = []
    for x in ItemInCategory.ERRORTYPE:
        if(x[0] != 'NONE'):
            list.append(x[0])
    return list


def getCount(masterid, errtype):
    '''
    Get the count of issues based on a site visited.
    '''

    if not errtype == 'NONE':
        count = InspectionDetails.objects.all().filter(
            master_id=masterid, item_id__errortype=errtype).count()
        return count
    pass


def getSum(self, errtype):
    if not errtype == 'NONE':
        # sum = InspectionDetails.objects.all().filter(
        #     master_id=masterid, item_id__errortype=errtype).count()

        if errtype == 'POWER':
            b1_error_messages = {'BN': 'B-N voltage not within limits - pls report to TNB.',
                                 'YN': 'Y-N voltage not within limits - pls report to TNB.',
                                 'RN': 'R-N voltage not within limits - pls report to TNB.'}

            b2_error_messages = {'R': 'Load on R-phase high - pls reduce/rebalance.',
                                 'Y': 'Load on Y-phase high - pls reduce/rebalance.',
                                 'B': 'Load on B-phase high - pls reduce/rebalance.'}

            b3_error_messages = {
                'PF': 'Low p.f. reading - pls rectify to avoid penalty.'}
            all_errors = [b1_error_messages,
                          b2_error_messages, b3_error_messages]
            # register the variables
            sum = 0
            distinctsites = set({})

            # issuecount = {key for key in b1_error_messages}
            issuecount = {}
            issuetop = []
            for each in all_errors:
                for keys in each:
                    details = InspectionDetails.objects.filter(
                        master_id__add_date__range=getstartq(self), item_id__items=keys)
                    if keys in b1_error_messages.keys():
                        for row in details:
                            if float(row.item_value) < 216.0 or float(row.item_value) > 253.0:
                                sum += 1
                                # print(
                                #     f"{keys} {row.item_value} - {each[keys]}")
                                distinctsites.add(row.master_id)
                                issuecount[keys] = issuecount.get(keys, 0) + 1
                                issuetop.append(b1_error_messages[keys])
                    if keys in b2_error_messages:
                        for row in details:
                            if float(row.item_value) >= 80:
                                sum += 1
                                # print(
                                #     f"{keys} {row.item_value} - {each[keys]}")
                                distinctsites.add(row.master_id)
                                issuecount[keys] = issuecount.get(keys, 0) + 1
                                issuetop.append(b2_error_messages[keys])
                    if keys in b3_error_messages:
                        for row in details:
                            if float(row.item_value) < 0.85:
                                sum += 1
                                # print(
                                #     f"{keys} {row.item_value} - {each[keys]}")
                                distinctsites.add(row.master_id)
                                issuecount[keys] = issuecount.get(keys, 0) + 1
                                issuetop.append(b3_error_messages[keys])
                    topissue = max(set(issuetop), key=issuetop.count)
                    distinctissue = len(issuecount)

            return {'sum': sum, 'ds': len(distinctsites), 'di': distinctissue, 'top': topissue}
        elif errtype == 'ENGINEERING':

            # item A.3 MSB year of installation - if result > 20 (years), then
            # MSB age > 20 years. (ENGINEERING, 2)
            sum = 0
            distinctsites = set({})
            issuecount = {}
            issuetop = []
            details = InspectionDetails.objects.all().filter(item_id__errortype=errtype, item_id__throw_error=True,
                                                             master_id__add_date__range=getstartq(self))
            sum = details.count()
            for each in details:
                distinctsites.add(each.master_id)
                issuecount[each.category_id] = issuecount.get(
                    each.item_id.items, 0) + 1
                issuetop.append(each.item_id.items)
            details = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self), item_id__items='MSB year of installation')

            datenow = datetime.now()
            for each in details:
                datadate = datetime.strptime(each.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datenow, datadate)
                if diffdate.years >= 20:
                    sum += 1
                    distinctsites.add(each.master_id)
                    # distinctissue += 1
                    # distinctsites.add(each.master_id)
                    issuecount[each.category_id] = issuecount.get(
                        each.item_id.items, 0) + 1
                    issuetop.append('MSB age > 20 years')
            distinctissue = len(issuecount)
            topissue = max(set(issuetop), key=issuetop.count)
            return {'sum': sum, 'ds': len(distinctsites), 'di': distinctissue, 'top': topissue}
        elif errtype == 'STATUTORY':

            sum = 0
            distinctsites = set({})
            issuecount = {}
            issuetop = []
            details = InspectionDetails.objects.all().filter(item_id__errortype=errtype, item_id__throw_error=True,
                                                             master_id__add_date__range=getstartq(self))
            sum = details.count()
            for each in details:
                distinctsites.add(each.master_id)
                issuecount[each.category_id] = issuecount.get(
                    each.item_id.items, 0) + 1
                issuetop.append(each.item_id.items)

            # item C.4 Due date - if result < 0, then
            # MSB relay overdue for calibration - pls arrange. (STATUTORY, 3)
            datenow = datetime.now()
            details = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self), item_id__items__contains='Due', category_id__category__contains='C.4')
            for each in details:
                datadate = datetime.strptime(
                    each.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sum += 1
                    distinctsites.add(each.master_id)
                    # distinctissue += 1
                    distinctsites.add(each.master_id)
                    issuecount[each.category_id] = issuecount.get(
                        each.item_id.items, 0) + 1
                    issuetop.append(
                        'MSB relay overdue for calibration - pls arrange.')

            # item c.5 Due date - if result < 0, then
            # Relay overdue for calibration - pls arrange. (STATUTORY, 3)
            details = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self), item_id__items__contains='Due', category_id__category__contains='C.5')

            for each in details:
                datadate = datetime.strptime(
                    each.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sum += 1
                    distinctsites.add(each.master_id)
                    # distinctissue += 1
                    distinctsites.add(each.master_id)
                    issuecount[each.category_id] = issuecount.get(
                        each.item_id.items, 0) + 1
                    issuetop.append(
                        'Relay overdue for calibration - pls arrange.')

            # item c.10 Due date - if result < 0, then
            # CO2 extinguisher overdue for certification - pls arrange. (STATUTORY, 3)
            details = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self), item_id__items__contains='Due', category_id__category__contains='C.10')

            for each in details:
                datadate = datetime.strptime(
                    each.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sum += 1
                    distinctsites.add(each.master_id)
                    # distinctissue += 1
                    distinctsites.add(each.master_id)
                    issuecount[each.category_id] = issuecount.get(
                        each.item_id.items, 0) + 1
                    issuetop.append(
                        'CO2 extinguisher overdue for certification - pls arrange.')

            # item c.17 Due date - if result < 0, then
            # Genset registration expired - pls renew with ST. (STATUTORY, 3)
            details = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self), item_id__items__contains='Due', category_id__category__contains='C.17')

            for each in details:
                datadate = datetime.strptime(
                    each.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sum += 1
                    distinctsites.add(each.master_id)
                    # distinctissue += 1
                    distinctsites.add(each.master_id)
                    issuecount[each.category_id] = issuecount.get(
                        each.item_id.items, 0) + 1
                    issuetop.append(
                        'Genset registration expired - pls renew with ST.')

            distinctissue = len(issuecount)
            topissue = max(set(issuetop), key=issuetop.count)
            return {'sum': sum, 'ds': len(distinctsites), 'di': distinctissue, 'top': topissue}
        else:
            details = InspectionDetails.objects.all().filter(item_id__errortype=errtype, item_id__throw_error=True,
                                                             master_id__add_date__range=getstartq(self))
            sum = details.count()
            distinctsites = details.distinct('master_id').count()
            try:
                distinctissue = details.distinct('item_id_id').count()
                topissue = details.annotate(countissue=Count(
                    'item_id_id')).order_by('-countissue')[0]
                # print(topissue.item_id.items)
                topissue = str(topissue.item_id.items)
            except IndexError:
                distinctissue = ''
                topissue = ''
            return {'sum': sum, 'ds': distinctsites, 'di': distinctissue, 'top': topissue}
    pass


class ShowDashboard(LoginRequiredMixin, FormView):
    template_name = 'inspectv1/dashboard_1.html'
    model = InspectionData
    form_class = DashboardDateFilterForm
    startdate = None
    enddate = None

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # context = super().get_context_data(**kwargs)
        # print(context)
        if 'dates' in request.POST:
            print("datefilter")
            print(request.POST['start_date'])

        else:
            print("filter quarter")

        if form.is_valid():
            print('xx', form)
        # context['form']=form
        return HttpResponse('0')

    def get_context_data(self, **kwargs):
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        # print(self.request.GET['start_date'])

        context = super().get_context_data(**kwargs)

        # load the datefilters with default values
        try:
            if self.request.GET['start_date']:
                self.startdate = (self.request.GET['start_date'])
                self.enddate = (self.request.GET['end_date'])
                initial_dict = {'start_date': self.startdate,
                                'end_date': self.enddate}
                form = DashboardDateFilterForm(None, initial=initial_dict)
                context['form'] = form

        except:
            initial_dict = {'start_date': getstartq(self)[0].strftime("%Y-%m-%d"),
                            'end_date': datetime.now().strftime("%Y-%m-%d")}
            form = DashboardDateFilterForm(None, initial=initial_dict)
            context['form'] = form

        listofsites = InspectionMaster.objects.filter(
            add_date__range=getstartq(self)).select_related().order_by('-id')

        # variable for location list
        data = {}
        error = {}
        locations = []
        names = []

        # location list for map markers
        locationlist = Sites.objects.filter(active=True)
        for loc in locationlist:
            locations.append({'lat': loc.latitude, 'lng': loc.longitude})
            names.append(loc.name)

        # count of types of issues and errors
        for errors in getERRTYPE():
            error[errors] = getSum(self, errors)
            data["errors"] = error

        # get the list of sites inspected
        # get count of sites and get percentage against sites in inspected which have data
        countofsites = Sites.objects.filter(active=True).count()
        countinspected = InspectionMaster.objects.filter(
            add_date__range=getstartq(self)).distinct().count()
        percentcompleted = (countinspected / countofsites) * 100

        # create boxplot get data for a field B.54 KVH
        categoryitems = InspectionCategory.objects.get(category='B.4 KWH')
        # print(categoryitems.id)
        categoryinspected = InspectionDetails.objects.all().select_related().filter(
            category_id__category='B.4 KWH', item_id__items='KWH')
        listing = []
        for item in categoryinspected:
            listing.append(float(item.item_value))

        # print(categoryinspected.aggregate(Max('item_value')))
        # print(categoryinspected.aggregate(Min('item_value')))
        # print(sum(listing) / len(listing))

        context["errors"] = error
        context['headers'] = getERRTYPE()
        context['locations'] = locations
        context['names'] = names
        context['countofsites'] = countofsites
        context['countinspected'] = countinspected
        context['percentcompleted'] = percentcompleted
        # context['form'] = form
        return context


class ShowDashboardDetails(LoginRequiredMixin, FormView):
    template_name = 'inspectv1/dashboard_2.html'
    form_class = DashboardDateFilterForm
    startdate = None
    enddate = None

    pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['key']  # get category of the search
        sitedata = []
        # set the datefilters
        try:
            if self.request.GET['start_date']:
                self.startdate = (self.request.GET['start_date'])
                self.enddate = (self.request.GET['end_date'])
                initial_dict = {'start_date': self.startdate,
                                'end_date': self.enddate}
                form = DashboardDateFilterForm(None, initial=initial_dict)
                context['form'] = form

        except:
            initial_dict = {'start_date': getstartq(self)[0].strftime("%Y-%m-%d"),
                            'end_date': datetime.now().strftime("%Y-%m-%d")}
            form = DashboardDateFilterForm(None, initial=initial_dict)
            context['form'] = form

        # get the sites related to the key
        sitesfound = InspectionDetails.objects.filter(
            item_id__errortype=category, item_id__throw_error=True, master_id__add_date__range=getstartq(self))
        risk = ['None', 'Low', 'Medium', 'High']
        for sites in sitesfound:
            data = {}
            subsidiary = str(sites.master_id.site_id.subsidiary)
            category = ' '.join(sites.category_id.category.split(' ')[1:])
            data["name"] = sites.master_id.site_id.name
            data["siteno"] = sites.master_id.site_id.site_no
            data["masterid"] = sites.master_id
            data["dateadd"] = sites.master_id.add_date
            data["category"] = category
            data["itemname"] = sites.item_id.items
            data["severity"] = risk[int(sites.item_id.severity)]
            data["state"] = sites.master_id.site_id.state
            data["subsidiary"] = subsidiary[subsidiary.find(
                "(")+1:subsidiary.find(")")]
            data["errortype"] = sites.item_id.errortype
            sitedata.append(data)
        context["sitedata"] = sitedata

        # get chart issues by site
        label = []
        data = []

        # chart data for issues
        chart_1 = sitesfound.values('item_id__items').annotate(
            total=Count('item_id')).order_by()
        for x in chart_1:
            if settings.DEBUG:
                print(x['item_id__items'], x['total'])
            label.append(x['item_id__items'])
            data.append(x['total'])

        context['issue_label'] = label
        context['issue_data'] = data

        # chart data for sites
        label2 = []
        data2 = []
        chart_2 = sitesfound.values('master_id__site_id__name').annotate(
            total=Count('item_id')).order_by()
        for x in chart_2:
            if settings.DEBUG:
                print(x['master_id__site_id__name'], x['total'])
            label2.append(x['master_id__site_id__name'])
            data2.append(x['total'])
        context['site_label'] = label2
        context['site_data'] = data2

        # chart data for category/field
        label3 = []
        data3 = []
        chart_3 = sitesfound.values('category_id__category').annotate(
            total=Count('item_id')).order_by()
        for x in chart_3:
            if settings.DEBUG:
                print(x['category_id__category'], x['total'])
            label3.append(' '.join(x['category_id__category'].split(' ')[1:]))
            data3.append(x['total'])
        context['cat_label'] = label3
        context['cat_data'] = data3

        # chart data for risk
        label4 = []
        data4 = []
        chart_4 = sitesfound.values('item_id__severity').annotate(
            total=Count('item_id')).order_by()
        for x in chart_4:
            if settings.DEBUG:
                print(x['item_id__severity'], x['total'])
            label4.append(risk[int(x['item_id__severity'])])
            data4.append(x['total'])
        context['risk_label'] = label4
        context['risk_data'] = data4

        # chart data for state
        label5 = []
        data5 = []
        chart_5 = sitesfound.values('master_id__site_id__state').annotate(
            total=Count('item_id')).order_by()
        for x in chart_5:
            if settings.DEBUG:
                print(x['master_id__site_id__state'], x['total'])
            label5.append(x['master_id__site_id__state'])
            data5.append(x['total'])
        context['state_label'] = label5
        context['state_data'] = data5

        # chart data for subsidiary
        label6 = []
        data6 = []
        chart_6 = sitesfound.values('master_id__site_id__subsidiary__name').annotate(
            total=Count('item_id')).order_by()
        for x in chart_6:
            # print(x['master_id__site_id__subsidiary__name'], x['total'])
            label6.append(x['master_id__site_id__subsidiary__name'])
            data6.append(x['total'])
        context['subsidiary_label'] = label6
        context['subsidiary_data'] = data6

        return context


def getstartq(self, **kwargs):
    current_date = datetime.now()
    current_quarter = round(((current_date.month - 1) // 3) + 1)

    first_date = datetime(current_date.year, 3 * current_quarter - 2, 1)
    last_date = datetime(current_date.year, 3 *
                         current_quarter % 12 + 1, 1) + timedelta(days=-1)
    # print(first_date, last_date)
    # print(self.startdate)
    # print(self.enddate)
    if 'startdate' in kwargs:
        if kwargs['startdate'] != '':
            # print(kwargs['startdate'])
            first_date = datetime.strptime(kwargs['startdate'], '%Y-%m-%d')
            last_date = datetime.strptime(kwargs['enddate'], '%Y-%m-%d')
    if (self.startdate):
        first_date = self.startdate
        last_date = self.enddate
    return (first_date, last_date)


def get_quarter_dates(year, quarter):

    selected_quarter = quarter
    first_date = datetime(year, 3 * quarter - 2, 1)
    last_date = datetime(year, 3 *
                         quarter % 12 + 1, 1) + timedelta(days=-1)
    return (first_date, last_date)


def distance(slat, slon, elat, elon):
    """
Function to get distance of 2 points
slat/slon - start lat , start lon - get this from the geolocation
elat,elon - pass the values from the database list
Sample code: refer distance.py
    """
    slat = radians(float(slat))
    slon = radians(float(slon))
    elat = radians(float(elat))
    elon = radians(float(elon))
    dist = 6371.01 * acos(sin(slat) * sin(elat) + cos(slat)
                          * cos(elat) * cos(slon - elon))
    return dist


@csrf_exempt
def getNearestSite(request):
    if request.method == 'POST':

        if request.POST.get('slat', False):
            slat = request.POST['slat']
            slon = request.POST['slon']
            sites = Sites.objects.filter(active=True)
            site_dict = {}

            for site in sites:
                dist = distance(slat, slon, site.latitude, site.longitude)
                # print('{}-{:.2f}'.format(site.id, dist))
                site_dict[site.site_no] = dist
                x = site_dict
                sorted_x = sorted(x.items(), key=lambda kv: kv[1])

            # print(sorted_x[:3]) #return closest 3 sites. the values from here are to be passed to UI for selection by the inspector
            countofsite = 4
            a_dict = [None]*countofsite
            countarr = 0
            for siteloc in sorted_x[:countofsite]:
                # print(siteloc[0])
                data = sites.get(site_no=siteloc[0])
                sitevalue = str(data.site_no) + '-' + str(data.name)
                b_dict = [None] * 3
                b_dict[0] = data.site_no
                b_dict[1] = data.name
                b_dict[2] = sitevalue
                a_dict[countarr] = b_dict
                # a_dict[1] = sitevalue
                countarr += 1
            # print(a_dict)

    return HttpResponse(json.dumps(a_dict))


class ShowInspectionDetails(LoginRequiredMixin, DetailView):
    template_name = 'inspectv1/sitedetails.html'
    model = InspectionMaster

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = InspectionCategory.objects.all().select_related()
        if settings.DEBUG:
            print("masterid", self.kwargs.get('pk', None))
        details = InspectionDetails.objects.filter(
            master_id=self.kwargs.get('pk', None)).select_related()
        siteid = InspectionMaster.objects.filter(
            id=self.kwargs.get('pk', None)).select_related()
        sites = Sites.objects.filter(id=siteid[0].site_id_id)
        for cat in category:
            for post in details:
                if cat.id == post.category_id_id:
                    cat.filled = 1

            for list in cat.items.all():
                # if list.fieldtype == 'checkbox':
                for post in details:
                    if post.item_id_id == list.id:
                        # if post.item_image:
                        if list.throw_error:
                            cat.iserror = 1
                        # else:
                        #    cat.iserror = 1
        context['posts'] = details
        context['category'] = category
        context['site_data'] = sites
        # category = category.union(details)
        return context


class TestForm(FormView):
    template_name = 'inspectv1/test.html'
    form_class = TestForm

    def post(self, request, *args, **kwargs):
        print('In post')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            print(form)
        return HttpResponseRedirect(reverse_lazy('inspectv1:test'))


def PowerDashboardErrors():
    error_messages = {'BN': 'B-N voltage not within limits - pls report to TNB.',
                      'YN': 'Y-N voltage not within limits - pls report to TNB.',
                      'RN': 'R-N voltage not within limits - pls report to TNB.'}
    data = Inspect

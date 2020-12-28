import os
import io
import json
from math import radians, acos, sin, cos
# import array as arr
from collections import Counter, OrderedDict
from datetime import datetime
import dateutil.relativedelta as delta
from dateutil.parser import parse
from mailmerge import MailMerge
import xlsxwriter
import pandas as pd
from django.conf import settings
from django.http import HttpResponse  # HttpResponseRedirect
from django.shortcuts import render  # , redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404
from django.db.models import Q, Count, FloatField  #Max, Min, Avg, , ,F
from django.db.models.functions import Cast
from django.views.generic.edit import FormView
from .models import InspectionCategory, InspectionDetails, InspectionMaster,\
    Sites, ItemInCategory, InspectorDetails
from .forms import DashboardDateFilterForm, InspectionData
# from django.contrib import messages
# from django.views.generic.edit import FormMixin
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile

# from django.urls import reverse_lazy


# Create your views here.


class IndexView(TemplateView):
    '''
    Display the landing page
    '''
    template_name = "inspectv1/index.html"


# class CreateInspectionForm(CreateView):
#     template_name = "inspectv1/inspection.html"
#     form_class = RunInspection


class ShowInspectionData(ListView):
    '''
    Display inspection data
    '''
    template_name = "inspectv1/updateinspection.html"
    # form_class = InspectionData

    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()


@login_required
def ShowInspectionDataFun(request):
    '''
    This is used to display the objects that are to bedisplayed in the
    checklist
    '''
    category = InspectionCategory.objects.all().select_related()

    my_param = request.GET.get('site')
    if my_param is None:
        return render(request, 'inspectv1/updateinspection.html',
                      {'category': category})

    # sites = Sites.objects.filter(site_no=request.GET['site'])
    sites = get_list_or_404(Sites, site_no=request.GET['site'])

    for site in sites:
        siteid = site.id
        # sitename = site.name

    inspectionmaster = InspectionMaster.objects.all().filter(
        user_id_id=request.user.id, site_id_id=siteid).select_related()
    master_id = 0

    for im in inspectionmaster:
        master_id = im.id

    if master_id == "0":
        return render(request, 'inspectv1/updateinspection.html',
                      {'category': category, 'site_data': sites})

    # posts = InspectedItem.objects.all().filter(user_id_id=request.user.id,
    # site_id_id = siteid ).select_related()
    posts = InspectionDetails.objects.all().filter(
        master_id_id=master_id).select_related()

    for cat in category:
        for post in posts:
            if cat.id == post.category_id_id:
                cat.filled = 1

        for lists in cat.items.all():
            # if list.fieldtype == 'checkbox':
            for post in posts:
                if post.item_id_id == lists.id:
                    # if post.item_image:
                    if lists.throw_error:
                        cat.iserror = 1
                    # else:
                    #    cat.iserror = 1

    return render(request, 'inspectv1/updateinspection.html',
                  {'category': category, 'posts': posts, 'site_data': sites})


@csrf_exempt
def GetCategories(request):
    if request.method == 'POST':
        # sites = Sites.objects.all().filter(site_no=request.POST['siteid'])
        site_count = Sites.objects.all().filter(
            site_no=request.POST['siteid']).count()
        category = InspectionCategory.objects.all()

        if site_count == 0:
            return HttpResponse(site_count)
        else:
            html = render_to_string(
                'inspectv1/createsite.html', {'sites': request.POST['siteid'],
                                              'category': category})
            return HttpResponse(html)
    else:
        return HttpResponse(0)


@csrf_exempt
def GetSites(request):
    if request.method == 'POST':
        totalsites = 0
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
        print(datetime.now(), "In Add")

    # return HttpResponse(request.POST['category_id'])

    if request.method == 'POST':
        current_user = request.user
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
        #     #     user_id_id=request.user.id, site_id_id=siteid,
        # add_date=dateadd).select_related()
        #     inspectionmaster = InspectionMaster.objects.get_or_create(
        #         user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
        # else:
        #     dateadd = None
        #     # inspectionmaster = InspectionMaster.objects.all().filter(
        #     # user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
        # .select_related()
        #     inspectionmaster = InspectionMaster.objects.get_or_create(
        #         user_id_id=request.user.id, site_id_id=siteid,
        #  add_date=dateadd)
        # # for im in inspectionmaster:
        # #     master_id = im.id
        # master_id = inspectionmaster[0].id
        if settings.DEBUG:
            print("DEBUG:masterid", master_id)
        # if 'dateadd' in request.POST:
        #     dateadd = request.POST['dateadd']
        #     # inspectionmaster = InspectionMaster.objects.all().filter(
        #     #     user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
        # .select_related()
        #     inspectionmaster = InspectionMaster.objects.get_or_create(
        #         user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
        #     master_id = inspectionmaster[0].id
        if request.POST['master_id'] == '':
            # master_id = 0
            if 'dateadd' in request.POST:
                dateadd = request.POST['dateadd']
            # inspectionmaster = InspectionMaster.objects.all().filter(
            #     user_id_id=request.user.id, site_id_id=siteid, add_date=dateadd)
            # .select_related()
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

                master_id_id=master_id, category_id_id=request.POST['category_id'])
            inspectDetailObj.delete()
        except:
            pass
        try:
            inspectDetailObj = InspectionDetails.objects.get(

                master_id_id=master_id, category_id_id=request.POST['category_id'],
                item_id_id=request.POST['item_id'])
            inspectDetailObj.item_value = request.POST['item_value']
            if bool(request.FILES.get('item_image', False)):
                inspectDetailObj.item_image = request.FILES['item_image']
            inspectDetailObj.save()
        except InspectionDetails.DoesNotExist:
            inspectDetailObj.master_id_id = master_id
            inspectDetailObj.category_id_id = request.POST['category_id']
            inspectDetailObj.item_id_id = request.POST['item_id']
            inspectDetailObj.item_value = request.POST['item_value']
            if bool(request.FILES.get('item_image', False)):
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
    if settings.DEBUG:
            print("DEBUG: Get Err Type",datetime.now())
    lists = [x[0] for x in ItemInCategory.ERRORTYPE if x[0] != 'NONE']
    # for x in ItemInCategory.ERRORTYPE:
    #     if x[0] != 'NONE':
    #         lists.append(x[0])
    return lists


def getCount(masterid, errtype):
    '''
    Get the count of issues based on a site visited.
    '''
    if settings.DEBUG:
            print("DEBUG: Start getCount",errtype,datetime.now())
    if not errtype == 'NONE':
        count = InspectionDetails.objects.all().filter(
            master_id=masterid, item_id__errortype=errtype).count()
        return count


def getSum(self, errtype):
    if settings.DEBUG:
            print("DEBUG: Start getSum",errtype,datetime.now())
    if not errtype == 'NONE':
        # sum = InspectionDetails.objects.all().filter(
        #     master_id=masterid, item_id__errortype=errtype).count()

        if errtype == 'POWER':
            if settings.DEBUG:
                print("DEBUG: Start getSum - POWER",errtype,datetime.now())
            b1_error_messages = {'BN': 'B-N voltage outside limits - report to TNB/SESB.',
                                 'YN': 'Y-N voltage outside limits - report to TNB/SESB.',
                                 'RN': 'R-N voltage outside limits - report to TNB/SESB.'}

            b2_error_messages = {'R': 'R-phase load high - reduce/rebalance.',
                                 'Y': 'Y-phase load high - reduce/rebalance.',
                                 'B': 'B-phase load high - reduce/rebalance.'}

            b3_error_messages = {
                'PF': 'Low PF reading - rectify to avoid penalty.'}
            all_errors = [b1_error_messages,
                          b2_error_messages, b3_error_messages]


            details = InspectionDetails.objects.filter(
                        master_id__add_date__range=getstartq(self),item_id__errortype=errtype).annotate(itemval = Cast('item_value',output_field=FloatField()))

            q1 = details.filter(item_id__items__in=b1_error_messages.keys()).filter(Q(itemval__lt=216)|Q(itemval__gt=253))


            q2 = details.filter(item_id__items__in=b2_error_messages.keys()).filter(Q(itemval__gte=80))

            q3 = details.filter(item_id__items__in=b3_error_messages.keys()).filter(Q(itemval__lt=0.85))


            # merged = q1.union(q2,q3)
            merged = q1|q2|q3
            allissuescount = merged.count()
            distinctsites = merged.values('master_id__site_id').distinct('master_id__site_id').count()
            distinctissues = merged.values('item_id__items').distinct('item_id__items').count()
            topissue = merged.values('item_id__items').annotate(numissues=Count('item_id__items')).order_by('-numissues')[:1]
            topissue = topissue[0]['item_id__items']
            for each in all_errors:
                try:
                    print(each,topissue)
                    if topissue in each.keys():
                        topissue = each[topissue]
                except:
                    pass
            riskids = list(merged.values_list('master_id__site_id_id','item_id_id','item_id__severity','item_id__items'))

            return {'sum': allissuescount, 'ds': distinctsites, 'di': distinctissues, 'top': topissue, 'risk': riskids}
        elif errtype == 'ENGINEERING':

            # item A.3 MSB year of installation - if result > 20 (years), then
            # MSB age > 20 years. (ENGINEERING, 2)
            # sums = 0
            # distinctsites = set({})
            # issuecount = {}
            # issuetop = []
            # riskids = []
            # if settings.DEBUG:
            #     print("DEBUG: Start getSum - start ENGINEERING",errtype,datetime.now())

            # details = InspectionDetails.objects.filter(item_id__errortype=errtype,
            #             item_id__throw_error=True, master_id__add_date__range=getstartq(self))
            # xsums = details.count()
            # xdistinctissues =details.distinct('item_id__items').count()

            # # for each in details:
            # #     distinctsites.add(each.master_id.site_id)
            # #     # issuecount[each.category_id] = issuecount.get(
            # #     #     each.item_id.items, 0) + 1
            # #     issuecount[each.item_id] = issuecount.get(
            # #         each.item_id.items, 0) + 1
            # #     sums += 1
            # #     issuetop.append(each.item_id.items)
            # #     riskids.append([each.master_id.site_id.id, each.item_id.id,
            # #                     each.item_id.severity, issuetop[-1]])

            # if settings.DEBUG:
            #     print("DEBUG: Start getSum - end ENGINEERING",errtype,datetime.now())


            # datenow = datetime.now()
            # datediff = datetime.strftime(datenow+delta.relativedelta(years=-20),"%Y-%m-%d")
            # print(datediff)
            # details2 = InspectionDetails.objects.filter(
            #     master_id__add_date__range=getstartq(self), item_id__items__contains='MSB year').filter(item_id__items__contains='MSB year').filter(item_value__lt=datediff)
            # xsums += details2.count()
            # xdistinctissues += details2.distinct('item_id__items').count()
            # xdistinctsites = details.distinct('master_id__site_id')
            # xdistinctsites2 = details2.distinct('master_id__site_id')
            # xdistinctsites3 = xdistinctsites.union(xdistinctsites2).distinct('master_id__site_id').count()
            # xtopissue = details.annotate(numissues=Count('item_id__items')).order_by('-numissues')[:1]
            # try:
            #     if len(xtopissue)  > 0:
            #         xtopissue = xtopissue[0].item_id.items
            #     else:
            #         xtopissue = None
            # except:
            #     pass
            # if settings.DEBUG:
            #     print("Debug - Engineering issues",xsums)
            #     print("Debug - Engineering distinct issue",xdistinctissues)
            #     print("Debug - Engineering distinct sites", xdistinctsites3)
            #     print('DEBUG - engineering xtopissue',xtopissue)


            # for each in details2:
            #     # datadate = datetime.strptime(each.item_value, "%Y-%m-%d")
            #     # diffdate = delta.relativedelta(
            #     #     datenow, datadate)
            #     # if diffdate.years >= 20:
            #     if True:
            #         sums += 1
            #         distinctsites.add(each.master_id.site_id)
            #         # distinctissue += 1
            #         # distinctsites.add(each.master_id)
            #         # issuecount[each.category_id] = issuecount.get(
            #         #     each.item_id.items, 0) + 1
            #         issuecount[each.item_id] = issuecount.get(
            #             each.item_id.items, 0) + 1
            #         # issuetop.append('MSB age > 20 years')
            #         # riskids.append([each.master_id.site_id.id, each.item_id.id,
            #                         # each.item_id.severity, issuetop[-1]])

            # distinctissue = len(issuecount)

            # # if len(issuetop) > 0:
            # #     topissue = max(set(issuetop), key=issuetop.count)
            # # else:
            #  #     topissue = None
            details = InspectionDetails.objects.filter(item_id__errortype=errtype,master_id__add_date__range=getstartq(self))

            # get all with error_true
            q1 = details.filter(item_id__throw_error=True)

            # get date value to compare
            datenow = datetime.now()
            datediff = datetime.strftime(datenow+delta.relativedelta(years=-20),"%Y-%m-%d")
            print(datediff)

            q2= details.filter(item_id__items__contains='MSB year').filter(item_value__lt=datediff)

            print("Details count with errtype",details.count())
            print("details with errors",q1.count())
            print("details with msb>20",q2.count())
            print(q2[0].item_id.items)


            merged = q1|q2
            allissuescount = merged.count()
            distinctsites = merged.values('master_id__site_id').distinct('master_id__site_id').count()
            distinctissues = merged.values('item_id__items').distinct('item_id__items').count()
            topissue = merged.values('item_id__items').annotate(numissues=Count('item_id__items')).order_by('-numissues')[:1]
            riskids = list(merged.values_list('master_id__site_id_id','item_id_id','item_id__severity','item_id__items'))
            print("All issues",allissuescount)
            print("distinct sites",distinctsites)
            print("distinct issues",distinctissues)
            print(topissue[0]['item_id__items'])
            # print("Top issue",topissue[0].item_id.items)


            all_errors = [{'MSB year of installation':'MSB age > 20 years'}]
            topissue = topissue[0]['item_id__items']
            # for each in merged:
            #     print(each.item_id.items)

            for each in all_errors:
                try:
                    print(each,topissue)
                    if topissue in each.keys():
                        topissue = each[topissue]
                except:
                    pass


            return {'sum': allissuescount, 'ds': distinctsites, 'di': distinctissues, 'top': topissue, 'risk': riskids}
        elif errtype == 'STATUTORY':

            if settings.DEBUG:
                print("DEBUG: Start getSum - STATUTORY",errtype,datetime.now())

            tagsdict = {'C.4':'MSB relay calibration expired - calibrate ASAP.',
                        'C.5':'Relay calibration expired - calibrate ASAP.',
                        'C.10':'CO2 extinguisher cert. expired - to recertify.',
                        'C.17':'Genset ST registration expired - to renew.'}
            todaydate = datetime.now().strftime('%Y-%m-%d')
            details = InspectionDetails.objects.filter(item_id__errortype='STATUTORY',master_id__add_date__range=getstartq(self))
            print("debug stat count",details.count())

            q1 = details.filter(item_id__throw_error=True)
            print("debug - throw error",q1.count())

            print(tagsdict.keys())


            for keys in tagsdict:
                q2 = details.filter(category_id__category__contains=keys,item_id__items__startswith='Due').filter(item_value__lt=todaydate)
                print(keys, q2.count())
            query=''
            q3 = details.filter(Q(category_id__category__contains='C.4')|Q(category_id__category__contains='C.5')|Q(category_id__category__contains='C.10')|Q(category_id__category__contains='C.17')).filter(item_id__items__startswith='Due').filter(item_value__lt=todaydate)
            print(q3.count())

            merged = q1|q3
            allissuescount = merged.count()
            distinctsites = merged.values('master_id__site_id').distinct('master_id__site_id').count()
            distinctissues = merged.values('category_id__category').distinct('item_id__items').count()
            topissue = merged.values('category_id__category','item_id__items').annotate(numissues=Count('item_id__items')).order_by('-numissues')[:1]
            riskids = list(merged.values_list('master_id__site_id_id','item_id_id','item_id__severity','item_id__items'))

            print("All issues",allissuescount)
            print("distinct sites",distinctsites)
            print("distinct issues",distinctissues)
            print("topissue",topissue[0]['category_id__category'])
            # print("Top issue",topissue[0].item_id.items)


            topcategory = topissue[0]['category_id__category']
            topissue = topissue[0]['item_id__items']
            # for each in merged:
            #     print(each.item_id.items)

            for key,value in tagsdict.items():
                try:
                    print(key,topcategory,topissue)
                    if topcategory.split()[0] in key:
                        topissue = value
                except:
                    pass
            print(topissue)

            return {'sum': allissuescount, 'ds': distinctsites, 'di': distinctissues, 'top': topissue, 'risk': riskids}
        elif errtype == 'RISK':
            riskids = []
            if settings.DEBUG:
                print("DEBUG: Start getSum - RISK",errtype,datetime.now())
            details = InspectionDetails.objects.all()\
                .filter(item_id__severity__gt=0,
                        master_id__add_date__range=getstartq(self))
            sums = details.count()
            distinctsites = details.distinct('master_id__site_id').count()
            try:
                distinctissue = details.distinct('item_id_id').count()

                topissue = details.annotate(countissue=Count(
                    'item_id_id')).order_by('-countissue')[0]
                # print(topissue.item_id.items)
                topissue = str(topissue.item_id.items)

            except IndexError:
                distinctissue = ''
                topissue = ''
            return {'sum': sums, 'ds': distinctsites, 'di': distinctissue, 'top': topissue, 'risk': riskids}
        else:
            # sums = 0
            # distinctsites = set({})
            # issuecount = {}
            # issuetop = []
            # riskids = []
            # if settings.DEBUG:
            #     print("DEBUG: Start getSum - ALL ELSE",errtype,datetime.now())
            # details = InspectionDetails.objects.all().filter(item_id__errortype=errtype, item_id__throw_error=True, master_id__add_date__range=getstartq(self))
            # # sums = details.count()
            # # distinctsites = details.distinct('master_id__site_id').count()
            # xdistinctsites = details.distinct('master_id__site_id').count()
            # xdistinctissues = details.distinct('item_id__items').count()
            # xissues = details.count()
            # xtopissue = details.annotate(numissues=Count('item_id__items')).order_by('-numissues')[:1]
            # try:
            #     if len(xtopissue[0].item_id.items)  > 0:
            #         xtopissue = xtopissue[0].item_id.items=""

            # except:
            #     pass
            # riskids = list(details.values_list('master_id__site_id_id','item_id_id','item_id__severity','item_id__items'))
            # if settings.DEBUG:
            #     print("Debug xdistinct sites",xdistinctsites)
            #     print("Debug xdistinct issues",xdistinctissues)
            #     print("DEbug xissues",xissues)
            #     print("Debug xtopissue",xtopissue)
                # print("Debug riskid",list(details.values_list('master_id__site_id_id','item_id_id','item_id__severity','item_id__items')))
            # for each in details:
                # distinctsites.add(each.master_id.site_id)
                # # issuecount[each.category_id] = issuecount.get(
                # #     each.item_id.items, 0) + 1
                # issuecount[each.item_id] = issuecount.get(
                #     each.item_id.items, 0) + 1
                # sums += 1
                # issuetop.append(each.item_id.items)
                # riskids.append([each.master_id.site_id.id, each.item_id.id,
                #                 each.item_id.severity, issuetop[-1]])
            # try:
            #     distinctissue = details.distinct('item_id_id').count()
            #     topissue = details.annotate(countissue=Count(
            #         'item_id_id')).order_by('-countissue')[0]
            #     # print(topissue.item_id.items)
            #     topissue = str(topissue.item_id.items)
            #     for each in details:
            #         riskids.append(riskids.append([each.master_id.site_id.id, each.item_id.id,
            #                                    each.item_id.severity, issuetop[-1]]))
            # except IndexError:
            #     distinctissue = ''
            #     topissue = ''
            # distinctissue = len(issuecount)

            # if len(issuetop) > 0:
            #     topissue = max(set(issuetop), key=issuetop.count)
            # else:
            #     topissue = ''
            # return {'sum': sums, 'ds': distinctsites, 'di': distinctissue, 'top': topissue, 'risks': riskids}
            details = InspectionDetails.objects.filter(item_id__errortype=errtype,master_id__add_date__range=getstartq(self))
            print("debug stat count",details.count())

            q1 = details.filter(item_id__throw_error=True)
            print("debug - throw error",q1.count())

            merged = q1
            allissuescount = merged.count()
            distinctsites = merged.values('master_id__site_id').distinct('master_id__site_id').count()
            distinctissues = merged.values('item_id__items').distinct('item_id__items').count()
            topissue = merged.values('category_id__category','item_id__items').annotate(numissues=Count('item_id__items')).order_by('-numissues')[:1]
            topissue = topissue[0]['item_id__items']
            return {'sum': allissuescount, 'ds': distinctsites, 'di': distinctissues, 'top': topissue, 'risk': ''}


def showmediafiles(sites):

    medialistall = []
    # try:
    #     if (sites.filter(category_id__category = '1.')):
    #         print('yes')
    # except Exception as e:
    #     print(e)
    #     pass
    if settings.DEBUG:
            print("DEBUG: Start media files",datetime.now())
    for site in sites:
        try:
            # print(site.item_id.items=='1.')
            if site.item_image:
                medialist = {}
                medialist['siteid'] = site.master_id.site_id.site_no
                medialist['sitename'] = site.master_id.site_id.name
                medialist['visitdate'] = site.master_id.add_date
                medialist['category']= site.item_id.items

                if medialist['category'].split(" ")[0].split(".")[0].isdigit():
                    for x in sites:
                        if x.item_id.items == medialist['category'].split(" ")[0] and x.master_id.site_id.site_no==medialist['siteid']:
                            # print(x.item_value)
                            medialist['category']=x.item_value


                medialist['url'] = site.item_image.url
                medialist['masterid']=site.master_id
                medialistall.append(medialist)
        except Exception as e:
            print(e)
            pass
    return medialistall


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
        # if 'dates' in request.POST:
        #     print("datefilter")
        #     print(request.POST['start_date'])

        # else:
        #     print("filter quarter")

        if form.is_valid():

            # print('xx', form)
            # context['form']=form
            return HttpResponse('0')

    def get_context_data(self, **kwargs):
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        # print(self.request.GET['start_date'])

        context = super().get_context_data(**kwargs)
        if settings.DEBUG:
            print("DEBUG: Start show dashboard",datetime.now())
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
                            'end_date': datetime.now().strftime("%Y-%m-%d")}  # 'end_date': datetime.now().strftime("%Y-%m-%d")
            form = DashboardDateFilterForm(None, initial=initial_dict)
            context['form'] = form

        # listofsites = InspectionMaster.objects.filter(
        #     add_date__range=getstartq(self)).select_related().order_by('-id')

        # variable for location list
        data = {}
        error = {}
        locations = []
        names = []

        # location list for map markers
        if settings.DEBUG:
            print("DEBUG: Start location markers",datetime.now())

        locationlist = Sites.objects.filter(active=True)
        locations=[{'lat':loc.latitude,'lng':loc.longitude} for loc in locationlist]
        names = [loc.name for loc in locationlist]
        # for loc in locationlist:
        #     locations.append({'lat': loc.latitude, 'lng': loc.longitude})
        #     names.append(loc.name)

        # count of types of issues and errors
        if settings.DEBUG:
            print("DEBUG: Start issues",datetime.now())
        for errors in getERRTYPE():
            error[errors] = getSum(self, errors)
            data["errors"] = error

        # get risk errors.
        if settings.DEBUG:
            print("DEBUG: Start get risks",datetime.now())
        sums = 0
        totalissue = []
        issue_to_display = []
        distinctsites = set({})
        for key, value in data['errors'].items():
            if value.get('risk') is not None:
                if len(value['risk']) > 0:
                    totalissue.extend(value['risk'])
                    # print(f"***RISK*** {key} {value['risk']} {len(value['risk'])}")

        issuetop = [issue[3] for issue in totalissue if issue[2] > 0]
        issuedict = dict(Counter(issuetop).items())
        issuedict_sort = sorted(issuedict.items(), key=lambda x: x[1], reverse=True)

        # print(issuedict_sort)

        for key, value in issuedict_sort[:3]:
            issue_to_display.append(key)

        sums = len(issuetop)
        distinctissue = len(set(issuetop))
        distinctsites = len(set([issue[0] for issue in totalissue]))

        if len(issuetop) > 0:
            topissue = max(set(issuetop), key=issuetop.count)
        else:
            topissue = ''

        context['RISK'] = {
            'sum': sums, 'ds': distinctsites, 'di': distinctissue, 'top': issue_to_display, 'risk': ''}

        # get the list of sites inspected
        # get count of sites and get percentage against sites in inspected which have data
        if settings.DEBUG:
            print("DEBUG: list of site inspected",datetime.now())

        countofsites = Sites.objects.filter(active=True).count()
        countinspected = InspectionMaster.objects.filter(
            add_date__range=getstartq(self)).distinct().count()
        percentcompleted = (countinspected / countofsites) * 100
        images = showmediafiles(InspectionDetails.objects.filter(
            master_id__add_date__range=getstartq(self)).select_related())
        totalissue = 0
        totaldistinctissue = 0
        for key,value in error.items():
            # print(key,value['di'])
            totalissue += value['sum']
            totaldistinctissue+=value['di']
            # print(key,value['ds'])

        context["errors"] = error
        context['headers'] = getERRTYPE()
        context['locations'] = locations
        context['names'] = names
        context['countofsites'] = countofsites
        context['countinspected'] = countinspected
        context['percentcompleted'] = percentcompleted
        context['totalissue']=totalissue
        context['totaldistinctissue']=totaldistinctissue
        context['item_imageurl'] = images

        # context['form'] = form
        if settings.DEBUG:
            print("DEBUG: End ShowDashboard",datetime.now())
        return context


def addtositedata(sites, *itemname):

    risk = ['None', 'Low', 'Medium', 'High']
    data = {}
    subsidiary = str(sites.master_id.site_id.subsidiary)
    category = ' '.join(sites.category_id.category.split(' ')[1:])
    category_code = sites.category_id.category.split(' ')[0]
    data["name"] = sites.master_id.site_id.name
    data["siteno"] = sites.master_id.site_id.site_no
    data["masterid"] = sites.master_id.id
    data["dateadd"] = datetime.strftime(sites.master_id.add_date, '%d/%m/%Y')

    try:
        dateval = datetime.strptime(sites.item_value, '%Y-%m-%d')
        if dateval:
            data['itemvalue'] = datetime.strftime(dateval, "%d/%m/%Y")
    except ValueError:
        data['itemvalue'] = sites.item_value
    if sites.item_value == 'true':
        data['itemvalue'] = ''
    data['category_code'] = category_code
    data["category"] = category
    if itemname:
        data["itemname"] = itemname[0]
    else:
        data["itemname"] = sites.item_id.items
    data["severity"] = risk[int(sites.item_id.severity)]
    data["state"] = sites.master_id.site_id.state
    data["subsidiary"] = subsidiary[subsidiary.find(
        "(")+1:subsidiary.find(")")]
    data["errortype"] = sites.item_id.errortype
    try:
        if sites.item_image.url:
            data["item_imageurl"] = sites.item_image.url
    except:
        pass
    # sitedata.append(data)
    return data


class ShowDashboardDetails(LoginRequiredMixin, FormView):
    template_name = 'inspectv1/dashboard_2.html'
    form_class = DashboardDateFilterForm
    startdate = None
    enddate = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkcategory = self.kwargs['key']  # get category of the search
        sitedata = []
        # risk = ['None', 'Low', 'Medium', 'High']
        # set the datefilters
        if settings.DEBUG:
            print("DEBUG: Start show dashboard details",datetime.now())
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
        if checkcategory == "POWER":
            # print("power")
            b1_error_messages = {'BN': 'B-N voltage outside limits - report to TNB/SESB.',
                                 'YN': 'Y-N voltage outside limits - report to TNB/SESB.',
                                 'RN': 'R-N voltage outside limits - report to TNB/SESB.'}

            b2_error_messages = {'R': 'R-phase load high - reduce/rebalance.',
                                 'Y': 'Y-phase load high - reduce/rebalance.',
                                 'B': 'B-phase load high - reduce/rebalance.'}

            b3_error_messages = {
                'PF': 'Low PF reading - rectify to avoid penalty.'}
            all_errors = [b1_error_messages,
                          b2_error_messages, b3_error_messages]
            for each in all_errors:
                querykey = each.keys()
                filterquery = Q(master_id__add_date__range=getstartq(
                    self)) & \
                    ((Q(item_id__items__in=querykey)))
                sitesfound = InspectionDetails.objects.filter(filterquery)
                for sites in sitesfound:
                    if sites.item_id.items in b2_error_messages.keys():
                        if float(sites.item_value) > 80:
                            # print(sites.item_id.items, sites.item_value,
                            #       sites.master_id.site_id.name)
                            sitedata.append(addtositedata(
                                sites, b2_error_messages[sites.item_id.items]))
                    if sites.item_id.items in b1_error_messages.keys():
                        if float(sites.item_value) < 216 or float(sites.item_value) > 253.0:
                            # print(sites.item_id.items, sites.item_value,
                            #       sites.master_id.site_id.name)
                            sitedata.append(addtositedata(
                                sites, b1_error_messages[sites.item_id.items]))
                    if sites.item_id.items in b3_error_messages.keys():
                        if float(sites.item_value) < 0.85:
                            # print(sites.item_id.items, sites.item_value,
                            #       sites.master_id.site_id.name)
                            sitedata.append(addtositedata(
                                sites, b3_error_messages[sites.item_id.items]))

        elif checkcategory == 'ENGINEERING':
            # print('engineering')
            sitesfound = InspectionDetails.objects.filter(
                item_id__errortype=checkcategory,
                item_id__throw_error=True, master_id__add_date__range=getstartq(self))
            for sites in sitesfound:
                sitedata.append(addtositedata(sites))

            # MSB year >20
            sitesfound = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self),
                item_id__items__contains='MSB year')
            datenow = datetime.now()
            for sites in sitesfound:
                datadate = datetime.strptime(sites.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datenow, datadate)
                if diffdate.years >= 20:
                    sitedata.append(addtositedata(sites, 'MSB age > 20 years'))

        elif checkcategory == 'STATUTORY':

            sitesfound = InspectionDetails.objects.filter(
                item_id__errortype=checkcategory,
                item_id__throw_error=True, master_id__add_date__range=getstartq(self))
            for sites in sitesfound:
                sitedata.append(addtositedata(sites))

            # # item C.4 Due date - if result < 0, then
            # MSB relay overdue for calibration - pls arrange. (STATUTORY, 3)
            sitesfound = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self),
                item_id__items__contains='Due', category_id__category__contains='C.4')
            datenow = datetime.now()
            for sites in sitesfound:
                datadate = datetime.strptime(sites.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sitedata.append(addtositedata(
                        sites, 'MSB relay calibration expired - calibrate ASAP.'))

            # item c.5 Due date - if result < 0, then
            # Relay overdue for calibration - pls arrange. (STATUTORY, 3)
            sitesfound = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self),
                item_id__items__contains='Due', category_id__category__contains='C.5')
            datenow = datetime.now()
            for sites in sitesfound:
                datadate = datetime.strptime(sites.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sitedata.append(addtositedata(
                        sites, 'Relay calibration expired - calibrate ASAP.'))

            # item c.10 Due date - if result < 0, then
            # CO2 extinguisher overdue for certification - pls arrange. (STATUTORY, 3)
            sitesfound = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self),
                item_id__items__contains='Due', category_id__category__contains='C.10')
            datenow = datetime.now()
            for sites in sitesfound:
                datadate = datetime.strptime(sites.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sitedata.append(addtositedata(
                        sites, 'CO2 extinguisher cert. expired - to recertify.'))

            # item c.17 Due date - if result < 0, then
            # Genset registration expired - pls renew with ST. (STATUTORY, 3)
            sitesfound = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self),
                item_id__items__contains='Due', category_id__category__contains='C.17')
            datenow = datetime.now()
            for sites in sitesfound:
                datadate = datetime.strptime(sites.item_value, "%Y-%m-%d")
                diffdate = delta.relativedelta(
                    datadate, datenow)
                if diffdate.days < 0:
                    sitedata.append(addtositedata(
                        sites, 'Genset ST registration expired - to renew.'))

        elif checkcategory == 'RISK':
            sitesfound = InspectionDetails.objects.filter(
                master_id__add_date__range=getstartq(self), item_id__severity__gt=0)

            for sites in sitesfound:
                sitedata.append(addtositedata(sites))

        else:
            sitesfound = InspectionDetails.objects.filter(
                item_id__errortype=checkcategory,
                item_id__throw_error=True, master_id__add_date__range=getstartq(self))
            for sites in sitesfound:
                sitedata.append(addtositedata(sites))
        context["sitedata"] = sitedata

        # chart data for issues
        label = []
        data = []
        chart1 = {}
        # chart_1 = sitesfound.values('item_id__items').annotate(
        #     total=Count('item_id')).order_by()
        for item in sitedata:
            # print(item)
            chart1[item['itemname']] = chart1.get(item['itemname'], 0)+1
        for key, val in chart1.items():
            # if settings.DEBUG:
            #     print(x['itemname'], x['itemname'].value())
            label.append(key)
            data.append(val)

        context['issue_label'] = label
        context['issue_data'] = data

        # chart data for sites
        label2 = []
        data2 = []
        chart2 = {}
        # chart_2 = sitesfound.values('master_id__site_id__name').annotate(
        #     total=Count('item_id')).order_by()\
        for item in sitedata:
            chart2[item['name']] = chart2.get(item['name'], 0)+1
        for key, val in chart2.items():
            # if settings.DEBUG:
            #     print(x['itemname'], x['itemname'].value())
            label2.append(key)
            data2.append(val)
        # for x in chart_2:
        #     if settings.DEBUG:
        #         print(x['master_id__site_id__name'], x['total'])
        #     label2.append(x['master_id__site_id__name'])
        #     data2.append(x['total'])
        context['site_label'] = label2
        context['site_data'] = data2

        # chart data for category/field
        label3 = []
        data3 = []
        chart3 = {}
        # chart_3 = sitesfound.values('category_id__category').annotate(
        #     total=Count('item_id')).order_by()
        # for x in chart_3:
        #     if settings.DEBUG:
        #         print(x['category_id__category'], x['total'])
        #     label3.append(' '.join(x['category_id__category'].split(' ')[1:]))
        #     data3.append(x['total'])

        # chart_2 = sitesfound.values('master_id__site_id__name').annotate(
        #     total=Count('item_id')).order_by()\
        for item in sitedata:
            chart3[item['category']] = chart3.get(item['category'], 0)+1
        for key, val in chart3.items():
            # if settings.DEBUG:
            #     print(x['itemname'], x['itemname'].value())
            label3.append(key)
            data3.append(val)
        context['cat_label'] = label3
        context['cat_data'] = data3

        # chart data for risk
        label4 = []
        data4 = []
        chart4 = {}
        # chart_4 = sitesfound.values('item_id__severity').annotate(
        #     total=Count('item_id')).order_by()
        # for x in chart_4:
        #     if settings.DEBUG:
        #         print(x['item_id__severity'], x['total'])
        #     label4.append(risk[int(x['item_id__severity'])])
        #     data4.append(x['total'])
        for item in sitedata:
            chart4[item['severity']] = chart4.get(item['severity'], 0)+1
        for key, val in chart4.items():
            # if settings.DEBUG:
            #     print(x['itemname'], x['itemname'].value())
            label4.append(key)
            data4.append(val)
        context['risk_label'] = label4
        context['risk_data'] = data4

        # chart data for state
        label5 = []
        data5 = []
        chart5 = {}
        #
        for item in sitedata:
            chart5[item['state']] = chart5.get(item['state'], 0)+1
        for key, val in chart5.items():
            # if settings.DEBUG:
            #     print(x['itemname'], x['itemname'].value())
            label5.append(key)
            data5.append(val)
        context['state_label'] = label5
        context['state_data'] = data5

        # chart data for subsidiary
        label6 = []
        data6 = []
        chart6 = {}
        #
        for item in sitedata:
            chart6[item['subsidiary']] = chart6.get(item['subsidiary'], 0)+1
        for key, val in chart6.items():
            # if settings.DEBUG:
            #     print(x['itemname'], x['itemname'].value())
            label6.append(key)
            data6.append(val)
        # chart_6 = sitesfound.values('master_id__site_id__subsidiary__name').annotate(
        #     total=Count('item_id')).order_by()
        # for x in chart_6:
        #     # print(x['master_id__site_id__subsidiary__name'], x['total'])
        #     label6.append(x['master_id__site_id__subsidiary__name'])
        #     data6.append(x['total'])
        context['subsidiary_label'] = label6
        context['subsidiary_data'] = data6

        if settings.DEBUG:
            print("DEBUG: End show dashboard details",datetime.now())
        return context


def getstartq(self, **kwargs):
    current_date = datetime.now()
    current_quarter = round(((current_date.month - 1) // 3) + 1)

    first_date = datetime(current_date.year, 3 * current_quarter - 2, 1)
    # last_date = datetime(current_date.year, 3 *
    #                      current_quarter % 12 + 1, 1) + timedelta(days=-1)
    last_date = first_date + delta.relativedelta(months=3, days=-1)
    # print(first_date, last_date)
    # print(self.startdate)
    # print(self.enddate)
    if 'startdate' in kwargs:
        if kwargs['startdate'] != '':
            # print(kwargs['startdate'])
            first_date = datetime.strptime(kwargs['startdate'], '%Y-%m-%d')
            last_date = datetime.strptime(kwargs['enddate'], '%Y-%m-%d')

    try:
        if self.startdate:
            first_date = self.startdate
            last_date = self.enddate
    except:
        pass

    return (first_date, last_date)


# def get_quarter_dates(year, quarter):

#     # selected_quarter = quarter
#     first_date = datetime(year, 3 * quarter - 2, 1)
#     last_date = datetime(year, 3 *
#                          quarter % 12 + 1, 1) + timedelta(days=-1)
#     return (first_date, last_date)


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

            # print(sorted_x[:3]) #return closest 3 sites. the values from here are
            # to be passed to UI for selection by the inspector
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

            for lists in cat.items.all():
                # if list.fieldtype == 'checkbox':
                for post in details:
                    if post.item_id_id == lists.id:
                        # if post.item_image:
                        if lists.throw_error:
                            cat.iserror = 1
                        # else:
                        #    cat.iserror = 1
        context['posts'] = details
        context['category'] = category
        context['site_data'] = sites
        # category = category.union(details)
        return context


class TestForm(TemplateView):
    template_name = 'inspectv1/test.html'


class PrintForm(LoginRequiredMixin, TemplateView):
    template_name = 'inspectv1/test.html'

    def get(self, request, *args, **kwargs):
        master_id = kwargs['key']
        template = os.path.join(settings.STATIC_ROOT,
                                'images/Blank_Form_I_template.docx')
        data = InspectionDetails.objects.filter(master_id=master_id)
        inspector = InspectorDetails.objects.get(
            users=data[0].master_id.user_id)
        issues = data.filter(item_id__show_in_section__gt=0)\
            .distinct('item_id')
        section1issues = [issue.item_id.items for issue in issues
                          .filter(item_id__show_in_section=1)]
        section2issues = [issue.item_id.items for issue in issues
                          .filter(item_id__show_in_section=2)]
        section3issues = [issue.item_id.items for issue in issues
                          .filter(item_id__show_in_section=3)]

        address = data[0].master_id.site_id.address
        certcompetency = inspector.com_lev
        certnumber = inspector.com_cert
        inspectiondate = data[0].master_id.add_date.strftime("%d / %m / %Y")
        inspectorname = inspector.users.first_name+' '+inspector.users.last_name
        siteaddress = data[0].master_id.site_id.address
        sitename = data[0].master_id.site_id.name
        stateauth = data[0].master_id.site_id.stoffice.location
        sitenum = data[0].master_id.site_id.site_no
        clientname = data[0].master_id.site_id.subsidiary.name
        section1issues = ', '.join(section1issues)
        section2issues = ', '.join(section2issues)
        section3issues = ', '.join(section3issues)

        document = MailMerge(template)

        document.merge(address=address,
                       certcompetency=certcompetency,
                       certnumber=certnumber,
                       inspectiondate=inspectiondate,
                       inspectorname=inspectorname,
                       siteaddress=siteaddress,
                       sitename=sitename,
                       stateauth=stateauth,
                       clientname=clientname,
                       section1issues=section1issues,
                       section2issues=section2issues,
                       section3issues=section3issues)
        date = datetime.now().strftime("%Y%m%d")
        filename = 'Form_I_' + str(sitenum) + '_' + date+'.docx'
        f = io.BytesIO()
        document.write(f)
        length = f.tell()
        f.seek(0)
        response = HttpResponse(
            f.getvalue(),
            content_type='application/vnd.openxmlformats -officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename='+filename
        response['Content-Length'] = length
        return response


@csrf_exempt
def DisplayIssueDetails(request):

    sitedata = []
    columns = ['Category', 'Items', 'Value', 'Category', 'Risk']
    if request:
        ids = request.POST['id']
        details = InspectionDetails.objects.filter(master_id=ids).order_by(('-id'))
        for x in details:
            sitedata.append(addtositedata(x))
        # sitedata[0]['dateadd'] = datetime.strftime(sitedata[0]['dateadd'], '%d/%m/%Y')
        return HttpResponse(json.dumps(sitedata))

    return None


class ShowInspectionDashboardTypeDetails(TemplateView):
    template_name = 'inspectv1/dashboard_2_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShowInspectionDashboardTypeDetails, self).get_context_data(**kwargs)
        sitedata = []
        pk = self.kwargs['pk']
        details = InspectionDetails.objects.filter(master_id=pk).order_by(('-id'))
        for x in details:
            sitedata.append(addtositedata(x))
        context["sitedata"] = sitedata
        return context

class GenerateExcelfile(LoginRequiredMixin,TemplateView):
    template_name = 'inspectv1/test.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
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
                            'end_date': datetime.now().strftime("%Y-%m-%d")}  # 'end_date': datetime.now().strftime("%Y-%m-%d")
            form = DashboardDateFilterForm(None, initial=initial_dict)
            context['form'] = form
        categories = InspectionCategory.objects.all()
        items = ItemInCategory.objects.all()
        sites = InspectionMaster.objects.filter(
            user_id=self.request.user.id, add_date__range=getstartq(self))
        siterowdata = []
        labels = ['Site No.','Station','State','Date']
        labels.extend([' '.join(category.category.split()[1:]) for category in categories])
        print('getting siterowdata listing')
        for site in sites:
            siterow=[]
            # print(site.site_id.site_no,site.site_id.name,site.site_id.state,site.add_date)
            siterow.extend([str(site.site_id.site_no),str(site.site_id.name),str(site.site_id.state),str(site.add_date)])

            for category in categories:

                items = InspectionDetails.objects.filter(master_id=site.id,category_id=category.id)
                # print(' '.join(str(category).split()[1:]))
                catdata = []
                for  item in items:
                    # print(item)
                    try:
                        if item.item_value:
                            # print(category.category, item.item_value)
                            # print(data[0].item_value)
                            value = item.item_value
                            if value == "true":
                                value = item.item_id.items
                                # print('value',value)
                            # siterow.append(value)
                            catdata.append(value)
                    except:
                        # siterow.append(' ')
                        # catdata.append(' ')
                        pass
                    # print(category,catdata)
                siterow.append("|".join(catdata))

            else:
                siterow.append(' ')

            siterowdata.append(siterow)
        print('generate excel')
        # create the file to be sent to download the excel file.
        f = io.BytesIO()
        workbook = xlsxwriter.Workbook(f,{'im_memory':True})
        worksheet = workbook.add_worksheet()
        maxrow = len(siterowdata)
        maxcol = len(siterowdata[0])
        row=0
        col=0

        for x in range(0,len(labels)):
            worksheet.write_string(row,col, labels[x])
            col+=1
        row=1
        for rows in range(0,maxrow):
            for cols in range(0,maxcol):
                worksheet.write_string(rows+1,cols, siterowdata[rows][cols])

        workbook.close()

        date = datetime.now().strftime("%Y%m%d")
        filename = 'Excel_download_' + date+'.xlsx'
        f.seek(0)
        response = HttpResponse(f.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename="+filename


        return response




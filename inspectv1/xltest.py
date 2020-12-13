
import os,sys
from datetime import datetime
import dateutil.relativedelta as delta
sys.path.append('/Users/vignes/Documents/Development/inspection')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inspection.settings")
import django
django.setup()
from math import radians, sin, cos, acos
from inspectv1.models import *
import inspectv1.views as views
import operator
import xlsxwriter

def getstartq():
    current_date = datetime.now()
    current_quarter = round(((current_date.month - 1) // 3) + 1)

    first_date = datetime(current_date.year, 3 * current_quarter - 2, 1)
    # last_date = datetime(current_date.year, 3 *
    #                      current_quarter % 12 + 1, 1) + timedelta(days=-1)
    last_date = first_date + delta.relativedelta(months=3, days=-1)
    return(first_date,last_date)

masterdata = InspectionMaster.objects.all()
datarecords = []
dataset = {}
categories = InspectionCategory.objects.all()
print(len(categories))
items = ItemInCategory.objects.all()

sites = InspectionMaster.objects.filter(add_date__range=getstartq())
siterowdata = []
labels = ['Site No.','Station','State','Date']
labels.extend([' '.join(category.category.split()[1:]) for category in categories])
print(len(labels))
print(labels)
for site in sites:
    siterow=[]
    # print(site.site_id.site_no,site.site_id.name,site.site_id.state,site.add_date)
    siterow.extend([str(site.site_id.site_no),str(site.site_id.name),str(site.site_id.state),str(site.add_date)])

    i=0
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

    siterowdata.append(siterow)      # print(items)



# for site in sites:
#     for category in categories:
#         items = ItemInCategory.objects.all().filter(category=category)
#         # print(category.category)
#         dataset[category.category]=None
#         itemvalues = []
#         for item in items:
#             # print(category.category,'**',item.items)
#             data = InspectionDetails.objects.filter(item_id=item.id,master_id=site.id)
#             try:
#                 if data[0].item_value:
#                     # print(data[0].item_value)
#                     value = data[0].item_value
#                     if value=="true":
#                         value = item.items
#                     itemvalues.append(value)
#             except:
#                 pass
#             dataset[category.category]=itemvalues
#         datarecords.append(dataset)
# print(datarecords)


workbook = xlsxwriter.Workbook('hello2.xlsx')
worksheet = workbook.add_worksheet()
date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
maxrow = len(siterowdata)
maxcol = len(siterowdata[0])
row=0
col=0
print('Rows')
for x in range(0,len(labels)):
    worksheet.write_string(row,col, labels[x])
    col+=1
row=1
for rows in range(0,maxrow):
    for cols in range(0,maxcol):
        worksheet.write_string(rows+1,cols, siterowdata[rows][cols])
        print(rows,cols,':',siterowdata[rows][cols])


workbook.close()



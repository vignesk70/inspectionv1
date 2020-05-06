from django.db import models
from django.conf import settings
from django.urls import reverse






# Create your models here.
class InspectionCategory(models.Model):

    category = models.CharField("Category", max_length=200)
    sequence = models.IntegerField("Sequence")
    

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['sequence',]

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})  

    def get_submit_status(self):
    	return "testtest"    
 
class ItemInCategory(models.Model):
    FIELDTYPE = ( ('checkbox','CheckBox'),
    ('text','Textfield'),('number','NumberField'),('date','DateField'))
    ERRORTYPE = [ ('NONE','None'),('STATUTORY','Statutory'),
    ('SAFETY','Safety'),('ENGINEERING','Engineering'),('OPERATIONS','Operations'),('POWER','Power')]

    category = models.ForeignKey("InspectionCategory", verbose_name="Category", on_delete=models.CASCADE, related_name='items', default=3)
    items = models.CharField("Item", max_length=200)
    show_in_section=models.IntegerField("Show in Section",default=0)
    throw_error = models.BooleanField("Throw error if True")
    sequence = models.IntegerField("Sequence")
    fieldtype = models.CharField(max_length=20, choices=FIELDTYPE) 
    errortype = models.CharField(max_length=20, choices=ERRORTYPE, default=' ', verbose_name="Category")
    severity = models.IntegerField("Risk Factors",default=0)
    
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['sequence',]

    def __str__(self):
        return self.items

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})

    def get_menu_choices(self):
        choices_tuple = []
        #do your stuff
        return choices_tuple

class Subsidiary(models.Model):
    name = models.CharField("name", max_length=100,default=" ")  
    class Meta:
        verbose_name = "Subsidiary"
        verbose_name_plural = "Subsidiary"
        
    def __str__(self):
        return self.name


class Stoffice(models.Model):
    location = models.CharField("location", max_length=100,default=" ")  
    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "ST Office"
        verbose_name_plural = "ST Office Locations"

class Sites(models.Model):
    
    site_no = models.IntegerField("Site Number")
    name = models.CharField("Site name", max_length=100)
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")
    state =  models.CharField("State", max_length=50)
    postcode = models.CharField("Postcode", max_length=20)
    address = models.CharField("Address", max_length=300)
    subsidiary = models.ForeignKey("Subsidiary", on_delete=models.CASCADE,  default=3)
    capacity=models.CharField("Capacity",max_length=300,default=' ')
    incomer=models.CharField("Incomer",max_length=300,default=' ')
    msbyear=models.CharField("Msb Year",max_length=300,default=' ')
    stoffice = models.ForeignKey("stoffice", on_delete=models.CASCADE,  default=3)



    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Site Details"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("site_detail", kwargs={"pk": self.pk})







class InspectorDetails(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    com_lev = models.CharField("Competency Level", max_length=200)
    com_cert = models.CharField("Competency Certificate", max_length=200)
    signature= models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    
    class Meta:
    	verbose_name = "Inspector Detail"
    	verbose_name_plural = "Inspector Details"
        

    def __str__(self):
        return str(self.users)


class CategoryFilterManager(models.Manager):
    def get_queryset(self):
    	return super().get_queryset() #.filter(category_id__id__exact = '6')




class InspectionMaster(models.Model):
    site_id = models.ForeignKey("Sites",  on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    add_date = models.DateField("Add Date", auto_now_add=True)
    update_date = models.DateField("Update Date",  auto_now_add=True)

    class Meta:
        verbose_name = "Inspection Result"
        verbose_name_plural = "Inspections Result"

    def __str__(self):
        return str(self.id)


class InspectionDetails(models.Model):
    master_id = models.ForeignKey("InspectionMaster", verbose_name="InspectionMaster", on_delete=models.CASCADE, related_name='details', default=3)
    category_id = models.ForeignKey("InspectionCategory",  on_delete=models.CASCADE)
    item_id = models.ForeignKey("ItemInCategory",  on_delete=models.CASCADE) #models.CharField("Item Id", max_length = 200)
    item_value = models.CharField("Item value", max_length = 500)
    item_image= models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    class Meta:
        verbose_name = "Detail"
        verbose_name_plural = "Details"

    def __str__(self):
        return self.item_value



class InspectedItem(models.Model):
    category_id = models.ForeignKey("InspectionCategory",  on_delete=models.CASCADE)
    site_id = models.ForeignKey("Sites",  on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_id = models.ForeignKey("ItemInCategory",  on_delete=models.CASCADE) #models.CharField("Item Id", max_length = 200)
    item_value = models.CharField("Item value", max_length = 500)
    item_image= models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    add_date = models.DateField("Add Date", auto_now_add=True)
    update_date = models.DateField("Update Date",  auto_now_add=True)

    objects = CategoryFilterManager()
    filter_objects = CategoryFilterManager() # The Dahl-specific manager.

    class Meta:
    	verbose_name = "Inspection Result"
    	verbose_name_plural = "Inspections Result"

    def __str__(self):
        return self.item_value    


class InspectItem(models.Model):
    inspector_name=models.CharField("Inspector Name",max_length=100,default=' ')
    category_name=models.CharField("Category Name",max_length=100,default=' ')
    site_name=models.CharField("Site Name",max_length=100,default=' ')
    Site_id=models.IntegerField("Site Id",default='0')
    Inspect_id=models.IntegerField("Inspector Id",default='0')
    Cat_id=models.IntegerField("Category Id",default='0')
    Item_id=models.IntegerField("Item Id",default='0')

    fieldname = models.CharField("value", max_length=100,default=" ")
    Items = models.CharField("items", max_length=100,default=" ")
    #sign=models.CharField("checked", max_length=100,default=" ")
    image= models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    class Meta:
        verbose_name = "Inspected Item"
        verbose_name_plural = "Inspected Items"

 

    def __str__(self):
        template = '{0.category_name} {0.site_name} {0.inspector_name}  {0.Items} {0.image}'
        return template.format(self)




        









    



    

from django.db import models

# Create your models here.
class InspectionCategory(models.Model):
    category = models.CharField("Category", max_length=50)
    

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})
 
class ItemInCategory(models.Model):
    category = models.ForeignKey("InspectionCategory", verbose_name="Items", on_delete=models.CASCADE)
    items = models.CharField("Item", max_length=20)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.items

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})

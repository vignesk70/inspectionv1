from django.db import models

# Create your models here.
class InspectionCatgory(models.Model):
    category = models.CharField("Category", max_length=50)
    

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})
 
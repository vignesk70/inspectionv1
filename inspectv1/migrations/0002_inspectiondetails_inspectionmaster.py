# Generated by Django 3.0.3 on 2020-04-23 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inspectv1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspectionMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_now_add=True, verbose_name='Add Date')),
                ('update_date', models.DateField(auto_now_add=True, verbose_name='Update Date')),
                ('site_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspectv1.Sites')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Inspection Result',
                'verbose_name_plural': 'Inspections Result',
            },
        ),
        migrations.CreateModel(
            name='InspectionDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_value', models.CharField(max_length=500, verbose_name='Item value')),
                ('item_image', models.ImageField(upload_to=None)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspectv1.InspectionCategory')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspectv1.ItemInCategory')),
                ('master_id', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='inspectv1.InspectionMaster', verbose_name='InspectionMaster')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
    ]

# Generated by Django 3.0.2 on 2020-02-14 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspectv1', '0005_auto_20200214_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspectItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Inspector_Name', models.CharField(default=' ', max_length=100, verbose_name='Inspector Name')),
                ('category_name', models.CharField(default=' ', max_length=100, verbose_name='Category Name')),
                ('site_name', models.CharField(default=' ', max_length=100, verbose_name='Site Name')),
                ('Site_id', models.IntegerField(default='0', verbose_name='Site Id')),
                ('Inspect_id', models.IntegerField(default='0', verbose_name='Inspector Id')),
                ('Cat_id', models.IntegerField(default='0', verbose_name='Category Id')),
                ('Item_id', models.IntegerField(default='0', verbose_name='Item Id')),
                ('fieldname', models.CharField(default=' ', max_length=100, verbose_name='value')),
                ('Items', models.CharField(default=' ', max_length=100, verbose_name='items')),
                ('image', models.ImageField(upload_to=None)),
            ],
            options={
                'verbose_name': 'Inspect_Item',
                'verbose_name_plural': 'Inspected Items',
            },
        ),
        migrations.DeleteModel(
            name='Inspect_Item',
        ),
        migrations.AlterModelOptions(
            name='inspectiondetails',
            options={'verbose_name': 'Inspector Detail', 'verbose_name_plural': 'Inspector Details'},
        ),
        migrations.AlterField(
            model_name='inspectiondetails',
            name='com_cert',
            field=models.CharField(max_length=200, verbose_name='Competency Certificate'),
        ),
        migrations.AlterField(
            model_name='inspectiondetails',
            name='com_lev',
            field=models.CharField(max_length=200, verbose_name='Competency Level'),
        ),
        migrations.AlterField(
            model_name='sites',
            name='stoffice',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='inspectv1.SToffice'),
        ),
    ]

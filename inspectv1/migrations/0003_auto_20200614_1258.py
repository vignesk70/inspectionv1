# Generated by Django 3.0.3 on 2020-06-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspectv1', '0002_inspectiondetails_inspectionmaster'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inspectiondetails',
            options={'verbose_name': 'Detail', 'verbose_name_plural': 'Details'},
        ),
        migrations.AddField(
            model_name='itemincategory',
            name='severity',
            field=models.IntegerField(default=0, verbose_name='Risk Factors'),
        ),
        migrations.AlterField(
            model_name='itemincategory',
            name='errortype',
            field=models.CharField(choices=[('NONE', 'None'), ('STATUTORY', 'Statutory'), ('SAFETY', 'Safety'), ('ENGINEERING', 'Engineering'), ('OPERATIONS', 'Operations'), ('POWER', 'Power')], default=' ', max_length=20, verbose_name='Category'),
        ),
    ]

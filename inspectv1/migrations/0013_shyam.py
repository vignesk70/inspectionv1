

# Generated by Django 3.0.3 on 2020-02-11 12:18


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspectv1', '0012_auto_20200129_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shyam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sno', models.CharField(default=' ', max_length=100, verbose_name='Site no')),
                ('items', models.CharField(default=' ', max_length=100, verbose_name='Site item')),
                ('site_field', models.CharField(default=' ', max_length=100, verbose_name='Site Field')),
            ],
            options={
                'verbose_name': 'Shyam',
                'verbose_name_plural': 'Shyams',
            },
        ),
    ]

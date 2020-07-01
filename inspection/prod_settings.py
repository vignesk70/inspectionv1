DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  'inspection',
        'USER': 'inspection',
        'PASSWORD': 'inspectionadmin',
        'HOST': 'inspection.grafnet.work',
        'PORT': '5432',
    }
}

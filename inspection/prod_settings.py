DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  'inspection',
        'USER': 'inspection',
        'PASSWORD': 'inspectionadmin',
        'HOST': 'app.navidadtech.com',
        'PORT': '5432',
    }
}

DEBUG = False
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
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'navidad.engineering@yahoo.com'
EMAIL_HOST_PASSWORD = 'jggsxjwidzsllhsc'
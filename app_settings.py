import os

app_env = os.environ.get('FLASK_ENV') or 'production'

if app_env == 'production':
    #PREFERRED_URL_SCHEME = "https"
    #SERVER_NAME = "archwomen.org"
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
if app_env == 'development':
    DEBUG = True
    SECRET_KEY = 'mysupersecretkeyisverysecure'
if app_env == 'testing':
    TESTING = True

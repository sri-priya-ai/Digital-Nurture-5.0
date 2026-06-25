# wsgi.py — Entry point for WSGI servers like gunicorn.
# Django hands off incoming HTTP requests through this object.
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
application = get_wsgi_application()

# asgi.py — Entry point for ASGI servers like uvicorn or daphne.
# Enables async views and WebSocket support when needed.
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
application = get_asgi_application()

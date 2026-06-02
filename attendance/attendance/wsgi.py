import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')

application = get_wsgi_application()

# Expose the WSGI application as 'app' for Vercel
app = application
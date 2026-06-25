# urls.py — Root URL config. Every request URL is matched here first.
# Using include() delegates /api/* URLs to the courses app's own urls.py,
# keeping each app's routing self-contained.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),  # mount all course routes under /api/
]

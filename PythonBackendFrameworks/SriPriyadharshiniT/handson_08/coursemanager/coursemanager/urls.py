from django.contrib import admin
from django.urls import path, include

# v1 prefix added — URL versioning is simple, visible, and browser-testable.
# Alternative: header versioning (Accept: application/vnd.api+json;version=1)
# keeps URLs cleaner but requires special tooling to test.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('courses.urls')),
]

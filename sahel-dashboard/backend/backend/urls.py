from django.contrib import admin
from django.urls import path, include  # Import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sahel_api.urls')),  # Include sahel_api URLs
]

# Serve media files during development
for static_dir in settings.STATICFILES_DIRS:
    urlpatterns += static(settings.STATIC_URL, document_root=static_dir)

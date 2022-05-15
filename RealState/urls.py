
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('property/', include('property.urls')),
                  path('', include('home.urls')),
                  path('dashboard/', include('dashboard.urls')),
                  path('mychat/', include('chat.urls')),
                  path('accounts/', include('accounts.urls')),
                  path('profile/', include('myprofile.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from profiles.views import all

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', all, name="home"),
    path('accounts/', include('registration.backends.default.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('questions/', include('questions.urls', namespace='questions')),
    path('directmessages/', include('directmessages.urls', namespace='directmessages')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

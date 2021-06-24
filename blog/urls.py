from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('post.urls')),
    path('api/ip/', include('views.urls')),
    path('textfield/', include('djrichtextfield.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


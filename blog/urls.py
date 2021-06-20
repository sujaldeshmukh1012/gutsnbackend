from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from django.contrib.auth import views as auth_views
from rest_framework.filters import SearchFilter

from authy.views import ApiUserProfile, UserProfile, UserProfileFavorites, login
from post.views import AllCategory, SearchView, AllProfiles, AllTag, IpTracker, apiOverview
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', apiOverview, name='api-overview'),
    path('blog/', include('post.urls')),
    path('user/', include('authy.urls')),
    path('<username>/saved', UserProfile, name='profilefavorites'),
    path('profile/<username>', ApiUserProfile, name='profile'),
    path('ip-track', IpTracker, name="TrackUserIps"),
    path('all-tags', AllTag, name="All Tags"),
    path('all-category', AllCategory, name="All Categories"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('accounts/', include('allauth.urls')),
    path('all-profiles/', AllProfiles.as_view(), name="All Profiles"),
    path('search/', SearchView.as_view(), name="Searching view"),
    path('textfield/', include('djrichtextfield.urls')),

    # path("",views.index,name="home"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

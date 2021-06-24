from views.views import IpModelIndex
from views.models import IpModel
from django.urls import path
from django.urls.conf import include



urlpatterns = [
    path('', IpModelIndex.as_view(), name="Index"),  
]

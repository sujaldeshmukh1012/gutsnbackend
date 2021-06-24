from django.urls import path
from django.urls.conf import include
from .views import PostDetails, TrendingAPI, index


urlpatterns = [
    path('blog/', index.as_view(), name="Index"),
    path('trending/', TrendingAPI.as_view(), name="Index"),
    path('blog/<slug:post_id>/', PostDetails.as_view(), name="Post Details"),
]

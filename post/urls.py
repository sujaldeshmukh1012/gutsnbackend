from django.urls import path
from django.urls.conf import include
from post.views import AllProfiles, PostComments, PostPostComments, TrendingAPI, UserLikes, apiOverview, index, NewPost, PostDetails, tags, home, favorite, likesObjDelete

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('<slug:post_id>', PostDetails.as_view(), name='postdetails'),
    path('<slug:post_id>/favorite', favorite, name='postfavorite'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
    path('comments/<slug:post_id>', PostComments.as_view(), name='post-comments'),
    path('comments/post/<slug:post_id>',
         PostPostComments.as_view(), name='post-comments'),
    path('likes/<str:post_id>', UserLikes.as_view(), name="User liked posts"),
    path('likes/delete/<str:post_id>',
         likesObjDelete, name="User liked posts"),
    path('trending/', TrendingAPI.as_view(), name="Trending blogs"),

]

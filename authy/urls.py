from django.urls import path
from authy.views import AllUserProfiles, ApiUserProfile, LoginAPI, ProfileAPI, RegisterAPI, UserAPI, UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile

from django.contrib.auth import views as authViews
from knox import views as knox_views


urlpatterns = [

    path('profile/edit', EditProfile, name='edit-profile'),
    path('signup/', Signup, name='signup'),
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(),
         {'next_page': 'index'}, name='logout'),
    path('changepassword/', PasswordChange, name='change_password'),
    path('changepassword/done', PasswordChangeDone, name='change_password_done'),
    path('passwordreset/', authViews.PasswordResetView.as_view(),
         name='password_reset'),
    path('passwordreset/done', authViews.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('passwordreset/<uidb64>/<token>/',
         authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/all', AllUserProfiles.as_view(), name='all-user'),
    path('api/profile/<str:username>/', ApiUserProfile, name='profile'),


]

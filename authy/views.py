from authy.serilizers import LoginSerializer, ProfileRequestSerializer, ProfileSerializer, UserSerializer, RegisterSerializer
from post.models import Post
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import Profile
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, request, response
from rest_framework.parsers import MultiPartParser, FormParser
from django.urls import reverse
from knox.models import AuthToken

from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.views import APIView

from django.urls import resolve
from django.contrib.auth import login as auth_login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

# api views
# @api_view(['GET'])
# def ApiUserProfile(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = Profile.objects.get(user=user)
#     # url_name = resolve(request.path).url_name
#     serializer = ProfileSerializer(profile, many=False)

#     return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def ApiUserProfile(request, username):
#     if request.method == 'GET':
#         user = get_object_or_404(User, username=username)
#         profile = Profile.objects.get(user=user)
#         serializer = ProfileSerializer(profile, many=False)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         user = get_object_or_404(User, username=username)
#         profile = Profile.objects.get(user=user)
#         serializer = ProfileSerializer(instance=profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @login_required
@api_view(['GET', 'PUT', 'DELETE'])
def ApiUserProfile(request, username):
    parser_classes = (MultiPartParser, FormParser)
    if request.user.username == username:
        user = request.user
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        try:
            profile = get_object_or_404(Profile, user=user)
        except profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProfileSerializer(
                profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


def login(request):
    return render(request, 'login.html')
    # class ApiUserProfile(APIView):
    #     """
    #     Retrieve, update or delete a snippet instance.
    #     """

    #     def get_user(self, request, username):
    #         me = request.user
    #         user = get_object_or_404(User, username=username)
    #         IsMe = False
    #         if me == user:
    #             IsMe = True
    #         else:
    #             IsMe = False
    #         return IsMe

    #     def get(self, request, username, format=None):
    #         user = get_object_or_404(User, username=username)
    #         profile = get_object_or_404(user)
    #         serializer = ProfileSerializer(profile)
    #         return Response(serializer.data)

    #     def put(self, request, username, format=None):
    #         user = get_object_or_404(User, username=username)
    #         profile = get_object_or_404(user)
    #         serializer = ProfileSerializer(profile, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     def delete(self, request, username, format=None):
    #         user = get_object_or_404(User, username=username)
    #         profile = get_object_or_404(user)
    #         profile.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         auth_login(request, user)
#         return super(LoginAPI, self).post(request, format=None)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    # def get_object(self):
    #     profile = Profile.objects.get(user=self.request.user)
    #     return ProfileSerializer(profile, many=False)

    def get_object(self):
        response = self.request.user
        return response


class AllUserProfiles(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        user_serializer = UserSerializer(user, many=True)
        profile = Profile.objects.all()
        profile_serializer = ProfileSerializer(profile, many=True)
        response = [[user_serializer.data] + [profile_serializer.data]]

        return Response(response)


class ProfileAPI(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, user, format=None):
        # user1 = self.request.user
        profile = Profile.objects.get(user=user)
        profile_serializer = ProfileSerializer(profile, many=False)
        return Response(profile_serializer.data)

    def put(self, request, user, format=None):
        # user1 = self.request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(
            profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# normal views


def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')

    else:
        posts = profile.favorites.all()

    # Profile info box
    posts_count = Post.objects.filter(user=user).count()

    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    template = loader.get_template('profile.html')

    context = {
        'posts': posts_paginator,
        'profile': profile,
        'posts_count': posts_count,
        'url_name': url_name,
    }

    return HttpResponse(template.render(context, request))


def UserProfileFavorites(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    posts = profile.favorites.all()

    # Profile info box
    posts_count = Post.objects.filter(user=user).count()

    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    template = loader.get_template('profile_favorite.html')

    context = {
        'posts': posts_paginator,
        'profile': profile,
        'posts_count': posts_count,
    }

    return HttpResponse(template.render(context, request))


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                username=username, email=email, password=password)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context)


def PasswordChangeDone(request):
    return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    BASE_WIDTH = 400

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('index')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'edit_profile.html', context)

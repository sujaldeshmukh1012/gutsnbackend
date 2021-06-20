from django.contrib.auth.models import User
from authy.serilizers import ProfileSerializer, UserSerializer
from comment.serilializers import CommentSerializer
from post.serializers import CategorySerializer, IpModelSerializer, LikesSerializer, PostSerializer, TagSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from django.template import loader

from post.models import Category, IpModel, Likes, Post, Tag
from post.forms import NewPostForm
from comment.models import Comment
from comment.forms import CommentForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache


from django.contrib.auth.decorators import login_required

from django.urls import reverse
from authy.models import Profile
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import filters

# api views

home = never_cache(TemplateView.as_view(template_name = 'index.html'))

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'All Posts': '/blog/',
        'Post Details': '/blog/<slug:post_id>',
        'Profile': '/profile/<username>',
        'Comments': '/blog/comments/<slug:post_id>',
        'All Ips': '/ ip-track /',
        'All Tags': '/all-tags',
        'All Categories': '/all-category'
    }

    return Response(api_urls)


# Create your views here.

class SearchView(generics.ListAPIView):
    search_fields = ['title', 'body']
    filter_backends = [filters.SearchFilter]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['GET'])
def IpTracker(request):
    Ip = IpModel.objects.all()
    serializer = IpModelSerializer(Ip, many=True)
    return Response(serializer.data)


class index(APIView):

    def get(self, request, format=None):
        def get_client_ip(request):
            address = request.META.get('HTTP_X_FORWARDED_FOR')
            if address:
                ip = address.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip

        ip = get_client_ip(request)
        q = IpModel.objects.filter(ip=ip).exists()
        if q:
            pass
        else:
            p = IpModel.objects.create(ip=ip)
            p.save()

        # user = request.user
        # profile = Profile.objects.get(user=user)
        # permission_classes = (AllowAny,)
        posts = Post.objects.all().reverse()
        serializer_post = PostSerializer(posts, many=True)
        # serializer_profile = ProfileSerializer(profile, many=False)

        # response = [serializer_post.data, [serializer_profile.data]]

        return Response(serializer_post.data)


class PostDetails(APIView):
    def get(self, request, post_id, format=None):
        def get_client_ip(request):
            address = request.META.get('HTTP_X_FORWARDED_FOR')
            if address:
                ip = address.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip

        ip = get_client_ip(request)
        a = IpModel.objects.create(ip=ip)
        a.save()
        q = IpModel.objects.filter(ip=ip).exists()
        if q == False:
            pass
        else:
            p = IpModel.objects.create(ip=ip)
            p.save()
        view_id = IpModel.objects.filter(ip=ip).last()
        post = Post.objects.get(id=post_id)
        user = Post.objects.get(id=post_id).user
        # user = request.user
        profile = Profile.objects.get(user=user)
        post_serializer = PostSerializer(post, many=False)
        profile_serializer = ProfileSerializer(profile, many=False)
        response = [post_serializer.data, profile_serializer.data]
        # response = post_serializer.data

        if post.views.filter(ip=view_id).exists():
            pass
        else:
            post.views.add(view_id)

        return Response(response)

    def put(self, request, post_id, format=None):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostComments(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.all().filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class PostPostComments(APIView):
    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            comments = Comment.objects.all().filter(post=post_id)
            serializer_class = CommentSerializer(comments, many=True)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllProfiles(APIView):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)


class AllUser(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def AllTag(request):
    tag = Tag.objects.all()
    serializer = TagSerializer(tag, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def AllCategory(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)


class UserLikes(generics.GenericAPIView):
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()

    def get(self, request, post_id):
        # user = request.user
        liked = Likes.objects.filter(post=post_id)
        serializer = LikesSerializer(liked, many=True)
        return Response(serializer.data)

    def post(self, request, post_id, * args, **kwargs):
        user = request.user
        id = request.data.get("post")
        post = Post.objects.get(id=post_id)
        action = request.data.get("delete")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        likes = serializer.save()
        posts = Post.objects.get(id=id)
        NoOf = Likes.objects.filter(post=posts).count()
        posts.likes = NoOf
        posts.save()

        liked = Likes.objects.filter(user=user, post=post_id)
        serializerClass = LikesSerializer(liked, many=True)

        return Response(serializerClass.data)


@api_view(['DELETE'])
def likesObjDelete(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    Like = Likes.objects.filter(post=post, user=user).delete()
    posts = Post.objects.get(id=post_id)
    NoOf = Likes.objects.filter(post=posts).count()
    posts.likes = NoOf
    posts.save()
    liked = Likes.objects.filter(user=user, post=post_id)
    serializer = LikesSerializer(liked, many=True)
    return Response(serializer.data)


class TrendingAPI(APIView):

    def get(self, request):
        posts = Post.objects.order_by('likes').order_by(
            'views').order_by('-posted')[:5]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# Normal views


@login_required
def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)

    else:
        profile.favorites.add(post)

    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))


@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        like.save()
        current_likes = current_likes + 1

    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))


def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    template = loader.get_template('tag.html')

    context = {
        'posts': posts,
        'tag': tag,
    }

    return HttpResponse(template.render(context, request))


@login_required
def NewPost(request):
    user = request.user.id
    tags_objs = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            p = Post.objects.get_or_create(
                picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)

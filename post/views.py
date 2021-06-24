from views.models import IpModel
from post.models import Post
from .serializers import PostSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

def get_client_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class index(APIView):

    def get(self, request, format=None):
        

        ip = get_client_ip(request)
        q = IpModel.objects.filter(ip=ip).exists()
        if q:
            pass
        else:
            p = IpModel.objects.create(ip=ip)
            p.save()
        posts = Post.objects.all().filter(isvisible=True).reverse()
        serializer_post = PostSerializer(posts, many=True)

        return Response(serializer_post.data)


class PostDetails(APIView):
    def get(self, request, post_id, format=None):
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
        post_serializer = PostSerializer(post, many=False)
        if post.views.filter(ip=view_id).exists():
                pass
        else:
            post.views.add(view_id)

        response = [post_serializer.data]
        return Response(response)

class TrendingAPI(APIView):

    def get(self, request):
        posts = Post.objects.order_by(
            'views').order_by('-posted')[:5]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

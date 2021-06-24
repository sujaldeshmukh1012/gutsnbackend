from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'posted', 'tags',
                  'categories', 'author', 'picture', 'likes', 'views', 'isvisible')

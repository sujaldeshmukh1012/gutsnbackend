from rest_framework import serializers
from .models import Category, IpModel, Likes, Post, Tag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'posted', 'tags',
                  'category', 'user', 'picture', 'likes', 'views')

    def save(self, *args, **kwargs):
        if self.instance.picture:
            self.instance.picture.delete()
        return super().save(*args, **kwargs)


class IpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpModel
        fields = ('id', 'ip', 'time')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ('id', 'post', 'user', 'delete')

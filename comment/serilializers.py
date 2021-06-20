from rest_framework import serializers
from .models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'body', 'parent', 'user',
                  'date')

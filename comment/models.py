from django.db import models
from post.models import Post
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete

# Create your models here.


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.id)


# Comment
# post_save.connect(Comment.user_comment_post, sender=Comment)
# post_delete.connect(Comment.user_del_comment_post, sender=Comment)

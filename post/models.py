from views.models import IpModel
from django.db import models


from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from autoslug import AutoSlugField
# Create your models here.


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.title, filename)


class Post(models.Model):
    picture = models.ImageField(
        upload_to=user_directory_path, verbose_name='Picture', null=False)
    title = models.TextField(
        max_length=500, verbose_name='Title', null=True)
    id = AutoSlugField(populate_from='title', primary_key=True)

    # body = models.TextField(
    #     max_length=10000, verbose_name='Body', null=False, default='')
    body = RichTextField(verbose_name='Body', null=False, default='')

    posted = models.DateTimeField(auto_now_add=True)
    tags = models.TextField(blank=True, default='blog')
    categories = models.TextField(blank=True, default='blog')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    views = models.ManyToManyField(
        IpModel, blank=True)
    isvisible = models.BooleanField(default=True, null=True)

    def get_absolute_url(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

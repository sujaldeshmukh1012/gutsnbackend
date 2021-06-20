import uuid
from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField


from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField


# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = AutoSlugField(populate_from='title')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=75, verbose_name='Category')
    slug = AutoSlugField(populate_from='title')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('Categories', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class IpModel(models.Model):
    ip = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip


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
    tags = models.ManyToManyField(Tag, related_name='tags')
    category = models.ManyToManyField(Category, related_name='category')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    views = models.ManyToManyField(
        IpModel, blank=True, related_name='post_views')

    def get_absolute_url(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class Likes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_like')
    delete = models.IntegerField(default=1, blank=True, null=True)

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender,
                              user=post.user, notification_type=1)
        notify.save()

    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        notify = Notification.objects.filter(
            post=post, sender=sender, notification_type=1)
        notify.delete()

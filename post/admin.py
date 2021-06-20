from django.contrib import admin
from post.models import Category, IpModel, Post, Tag, Likes

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'posted', 'user', 'likes')
    list_filter = ('views', 'likes', 'id')
    search_fields = ('id', 'title', 'views', 'body')
    ordering = ('-posted',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_filter = ('id', 'title', 'slug')
    search_fields = ('id', 'title', 'slug')
    ordering = ('-id',)


class LikesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'delete')
    list_filter = ('id', 'user', 'post')
    search_fields = ('id', 'user', 'post')
    ordering = ('-id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_filter = ('id', 'title', 'slug')
    search_fields = ('id', 'title', 'slug')
    ordering = ('-id',)


class IpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'time')
    list_filter = ('id', 'ip', 'time')
    search_fields = ('id', 'ip', 'time')
    ordering = ('-time',)


admin.site.register(IpModel, IpAdmin)
admin.site.register(Likes, LikesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

from .models import Post
from django.contrib import admin

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'posted', 'author', 'likes')
    list_filter = ('views', 'likes', 'id')
    search_fields = ('id', 'title', 'views', 'body')
    ordering = ('-posted',)


admin.site.register(Post, PostAdmin)

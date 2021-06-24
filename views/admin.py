from .models import IpModel
from django.contrib import admin

# Register your models here.


class IpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'time')
    list_filter = ('id', 'ip', 'time')
    search_fields = ('id', 'ip', 'time')
    ordering = ('-time',)




admin.site.register(IpModel, IpAdmin)

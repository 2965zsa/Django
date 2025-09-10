from django.contrib import admin
from .models import BlogCommit,BlogContent,Categote
# Register your models here.


class BlogCommitAdmin(admin.ModelAdmin):

    list_display = ['time','commit','user','blog']


class BlogContentAdmin(admin.ModelAdmin):
    list_display = ['title','category','time','content','user']
class CategoteAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(BlogCommit,BlogCommitAdmin)
admin.site.register(Categote,CategoteAdmin)
admin.site.register(BlogContent,BlogContentAdmin)
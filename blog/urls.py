from django.urls import path
from . import views

app_name='blog'
urlpatterns = [
    path('', views.index, name='index'),

    path('blog/detail/<int:blog_id>', views.blog_detail, name='blog_detail'),

    path('blog/pub_blog', views.pub_blog, name='pub_blog'),

    path('blog/commit', views.blog_commit, name='blog_commit'),

    path('search', views.search, name='search'),
]
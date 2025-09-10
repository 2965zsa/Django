from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Categote(models.Model):
    name = models.CharField(max_length=200,verbose_name='分类')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog.categote'
        verbose_name='分类'
        verbose_name_plural=verbose_name

class BlogContent(models.Model):
    title = models.CharField(max_length=200,verbose_name='博客标题')
    content = models.TextField(verbose_name='博客内容')
    time=models.DateTimeField(auto_now_add=True,verbose_name='博客发布时间')
    category = models.ForeignKey(Categote, on_delete=models.CASCADE,verbose_name='文章分类')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='博客作者')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='发布博客'
        db_table = 'blog.Content'
        verbose_name_plural=verbose_name
        ordering=['-time']


class BlogCommit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='评论作者')
    time=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    commit = models.TextField(verbose_name='评论内容')
    blog = models.ForeignKey(BlogContent, on_delete=models.CASCADE,related_name='commits',verbose_name='博客作者')

    def __str__(self):
        return self.commit

    class Meta:
        db_table = 'blog.Commit'
        verbose_name='评论内容'
        verbose_name_plural=verbose_name
        ordering=['-time']
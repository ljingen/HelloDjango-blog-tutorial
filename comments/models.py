from django.db import models
from django.utils import timezone
# Create your models here.

from blog.models import Post


class Comment(models.Model):
    """评论的数据库"""
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return '{}:{}'.format(self.name, self.text[:20])

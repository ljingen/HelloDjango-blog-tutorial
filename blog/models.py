from datetime import datetime
import markdown

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from mdeditor.fields import MDTextField


# Create your models here.


class Category(models.Model):
    """
    django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """
    name = models.CharField('分类', max_length=100)
    desc = models.CharField('描述', max_length=300, blank=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField('标签', max_length=100)
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章的数据库表稍微复杂一些,主要是设计的字段较多
    """
    # 文章标题
    title = models.CharField('标题', max_length=70)
    body = MDTextField('正文')  # MDTextField   markdown 字段(将之前的models.TextField() 改成 MDTextField)

    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间', default=timezone.now)
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    # 新增views字段记录阅读数量
    click_nums = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        self.excerpt = strip_tags(md.convert(self.body))[:154]
        super().save(*args, **kwargs)

    # 自定义get_absolute_url方法
    # 记得从django.url中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_click_nums(self):
        self.click_nums += 1
        self.save(update_fields=['click_nums'])

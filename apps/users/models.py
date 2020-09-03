from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    # 性别选择器
    SEX_IN_USER_CHOICES = (
        ('male', u'男'),
        ('female', u'女'),
    )
    gender = models.CharField(
        max_length=6,
        verbose_name=u'性别',
        choices=SEX_IN_USER_CHOICES,
        default='male'
    )
    nickname = models.CharField('昵称', max_length=50, blank=True, null=True)
    birthday = models.DateField(verbose_name=u'生日', default=timezone.now)
    address = models.CharField(max_length=100, verbose_name=u'地址', default=u'')
    mobile = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    image = models.ImageField(max_length=100, upload_to='image/%Y/%M/%D', default=u'image/default.png',verbose_name=u'用户头像')
    sign = models.CharField(max_length=100, verbose_name='个性签名', null=True, blank=True,default=u'这家伙很懒,什么都没留下')
    classroom = models.CharField(max_length=2, verbose_name='班级', null=True, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'标题')
    image = models.ImageField(upload_to='image/%Y/%M/%D', verbose_name=u'轮播图', max_length=100)
    url = models.URLField(max_length=100, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    created_time= models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework import routers

from blog.api_views import PostViewSet, CategoryViewSet, TagViewSet
from comments.api_views import CommentViewSet
router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('categories', CategoryViewSet, basename='category')
router.register('tags', TagViewSet, basename='tag')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path(r'', include('blog.urls')),
    path('admin/', admin.site.urls),
    path(r'blog/', include('blog.urls')),
    path(r'comments/', include('comments.urls')),
    path(r'users/', include('users.urls')),
    # 登录，修改密码，找回密码等视图函数使用django自带的
    path(r'users/', include('django.contrib.auth.urls')),

    path(r'mdeditor', include('mdeditor.urls')),

    # api接口
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 关于页面
    path('about/', TemplateView.as_view(template_name='blog/about.html')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

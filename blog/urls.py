from django.urls import path

from . import views, api_views

# 视图函数命名空间
app_name = 'blog'
urlpatterns = [
    # 使用函数模式
    # path('', views.index, name='index'),
    # path('categories/<int:pk>/', views.category, name='category'),
    # path('tags/<int:pk>/', views.tag, name='tag'),
    # path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    # path('posts/<int:pk>/', views.detail, name='detail'),
    path('serach/', views.search, name='search'),

    # 使用类视图模式
    path('', views.IndexView.as_view(), name='index'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),

    # api接口
    path('api/index/', api_views.index_view),

]

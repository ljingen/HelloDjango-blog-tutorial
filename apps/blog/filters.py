from django_filters import rest_framework as drf_filters
from .models import Post


class PostFilter(drf_filters.FilterSet):
    """
    django-filter 实际上会将以上定义的规则翻译为如下的 ORM 查询语句：
    Post.objects.filter(created_time__year=created_year传递的值)
    """
    created_year = drf_filters.NumberFilter(field_name="created_time",
                                            lookup_expr="year")
    created_month = drf_filters.NumberFilter(field_name="created_time",
                                             lookup_expr="month")

    class Meta:
        model = Post
        fields = ['category', "tags", "created_year", "created_month"]

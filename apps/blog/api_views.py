from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.serializers import DateField
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Category, Tag
from .filters import PostFilter
from .serializers import PostListSerializer, PostRetriveSerializer, CategorySerializer, TagSeiralizer
from comments.serializers import CommentSerializer
from comments.models import Comment


@api_view(http_method_names=["GET"])
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    serializer = PostListSerializer(post_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class IndexPostListAPIView(ListAPIView):
    serializer_class = PostListSerializer  # 指定序列化器
    queryset = Post.objects.all()  # 序列化内容
    pagination_class = PageNumberPagination  # 对资源分页
    permission_classes = [AllowAny]  # 权限设置


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter

    # 后续对于其他动作，可以再加 elif 判断，不过如果动作变多了，就会有很多的 if 判断
    # 更好的做好是，给视图集加一个属性，用于配置 action 和 serializer_class 的对应关系，
    # 通过查表法查找 action 应该使用的序列化器
    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve': PostRetriveSerializer,
    }

    #  动态Serializer
    def get_serializer_class(self):
        """
        HTTP请求对应的action关系
        GET  list(资源列表)/retrieve(单个资源)
        PUT  update
        PATCH partial_update
        DELETE  destory
        """
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostRetriveSerializer
        else:
            return super().get_serializer_class()

    @action(
        methods=["GET"],
        detail=False,
        url_path="archive/dates",
        url_name="archive-date")
    def list_archive_date(self, request, *args, **kwargs):
        dates = Post.objects.dates("created_time", "month", order="DESC")
        date_field = DateField()
        data = [date_field.to_representation(date) for date in dates]
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_path="comments",
        url_name="comment",
        pagination_class=LimitOffsetPagination,
        serializer_class=CommentSerializer,
    )
    def list_comments(self, request, *args, **kwargs):
        # 根据url传递的参数值(文章id)获取到博客文章记录
        post = self.get_object()
        # 获取文章下面的关联全部评论
        queryset = post.comment_set.all().order_by("-created_time")
        # 对评论列表进行分页，根据url传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = self.get_serializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        elif self.action == 'retrieve':
            return CategorySerializer
        else:
            return super().get_serializer_class()


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSeiralizer
    queryset = Tag.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return TagSeiralizer
        elif self.action == 'retrieve':
            return TagSeiralizer
        else:
            return super().get_serializer_class()


# 演示ViewSet如何绑定方法
index_view = PostViewSet.as_view({'get': 'list'})

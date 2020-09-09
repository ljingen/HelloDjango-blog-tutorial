from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import mixins

from .models import Post
from .serializers import PostListSerializer, PostRetriveSerializer


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


class IndexPostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    # 后续对于其他动作，可以再加 elif 判断，不过如果动作变多了，就会有很多的 if 判断
    # 更好的做好是，给视图集加一个属性，用于配置 action 和 serializer_class 的对应关系，
    # 通过查表法查找 action 应该使用的序列化器

    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve':PostRetriveSerializer,
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


# 演示ViewSet如何绑定方法
index_view = IndexPostViewSet.as_view({'get': 'list'})

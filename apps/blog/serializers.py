from rest_framework import serializers
from .models import Post, Category, Tag
from users.models import User


class TagSeiralizer(serializers.ModelSerializer):
    """标签序列化器"""

    class Meta:
        model = Tag
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    """列表序列号器"""

    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname']


class PostListSerializer(serializers.ModelSerializer):
    """文章列表序列化器"""
    category = CategorySerializer()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_time', 'excerpt', 'click_nums', 'category', 'author']


class PostRetriveSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    category = CategorySerializer()
    author = UserSerializer()
    tags = TagSeiralizer(many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "created_time", "modified_time", "excerpt",
                  "click_nums", "category", "author", "tags"]

from rest_framework import mixins, viewsets
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

from rest_framework.generics import ListCreateAPIView
from .serializers import PostsSerializer
from .models import Post


class PostListViewSet(ListCreateAPIView):
    """
    API endpoint that allows users to see some post.
    """
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

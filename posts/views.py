from django.views.generic import ListView
from posts.models import Post


class PostListView(ListView):

    model = Post
    template_name = 'index.html'

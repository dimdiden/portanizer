from django.conf.urls import url
from posts.views import PostListView


urlpatterns = [
    url(r'^$', PostListView.as_view(), name='index'),
]

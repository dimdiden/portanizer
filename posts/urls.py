from django.conf.urls import url
from posts.views import (
    PostListView,
    CreatePostView,
    UpdatePostView,
    CreateTagView,
    DeletePostView,
)

urlpatterns = [
    url(r'^$',
        PostListView.as_view(), name='index'),
    url(r'^createpost/',
        CreatePostView.as_view(), name='createpost'),
    url(r'^updatepost/(?P<pk>[0-9]+)/',
        UpdatePostView.as_view(), name='updatepost'),
    url(r'^deletepost/(?P<pk>[0-9]+)/',
        DeletePostView.as_view(), name='deletepost'),
    url(r'^createtag/',
        CreateTagView.as_view(), name='createtag'),
]

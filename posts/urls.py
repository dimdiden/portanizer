from django.conf.urls import url
from .views import (
    PostListView,
    CreatePostFormView,
    UpdatePostFormView,
    TagManagerView,
    DeletePostView,
)

from .viewsets import PostListViewSet

urlpatterns = [
    url(r'^$',
        PostListView.as_view(), name='index'),
    url(r'^create/',
        CreatePostFormView.as_view(), name='create'),
    url(r'^update/(?P<pk>[0-9]+)/',
        UpdatePostFormView.as_view(), name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/',
        DeletePostView.as_view(), name='delete'),
    url(r'^tagmanager/$',
        TagManagerView.as_view(), name='tagmanager'),
    url(r'^api/$',
        PostListViewSet.as_view(), name='post_api'),
]

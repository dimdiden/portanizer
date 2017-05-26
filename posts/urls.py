from django.conf.urls import url
from posts.views import (
    PostListView,
    CreatePostFormView,
    UpdatePostFormView,
    # CreateTagView,
    UpdateTagFormView,
    DeletePostView,
    DeleteTagView,
)

urlpatterns = [
    url(r'^$',
        PostListView.as_view(), name='index'),
    url(r'^createpost/',
        CreatePostFormView.as_view(), name='createpost'),
    url(r'^updatepost/(?P<pk>[0-9]+)/',
        UpdatePostFormView.as_view(), name='updatepost'),
    url(r'^deletepost/(?P<pk>[0-9]+)/',
        DeletePostView.as_view(), name='deletepost'),
    # url(r'^createtag/',
    #     CreateTagView.as_view(), name='createtag'),
    url(r'^tagmanager/$',
        UpdateTagFormView.as_view(), name='tagmanager'),
    url(r'^tagmanager/(?P<pk>[0-9]+)/',
        UpdateTagFormView.as_view(), name='tagmanager_upd'),
    url(r'^tagmanager/delete/(?P<pk>[0-9]+)/',
        DeleteTagView.as_view(), name='tagmanager_del'),
]

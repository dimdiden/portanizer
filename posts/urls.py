from django.conf.urls import url
from posts.views import IndexTemplateView


urlpatterns = [
    url(r'^$', IndexTemplateView.as_view(), name='index'),
]

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',
        RedirectView.as_view(pattern_name='posts:index')),
    url(r'^authorization/',
        include('authorization.urls', namespace='authorization')),
    url(r'^posts/', include('posts.urls', namespace='posts')),
]

from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import UserLoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^', include('posts.urls')),
]

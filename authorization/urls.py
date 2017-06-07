from django.conf.urls import url
from authorization.views import UserLoginView, UserRegisterView, LogoutView

urlpatterns = [
    url(r'^login/', UserLoginView.as_view(), name='login'),
    url(r'^register/', UserRegisterView.as_view(), name='register'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
]

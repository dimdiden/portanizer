from django.conf.urls import url
from authorization.views import (
    UserLoginView,
    UserRegisterView,
    LogoutView,
    ResetpwdView,
    ResetpwdConfirmView
)

urlpatterns = [
    url(r'^login/', UserLoginView.as_view(), name='login'),
    url(r'^register/', UserRegisterView.as_view(), name='register'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^resetpwd/$', ResetpwdView.as_view(), name='resetpwd'),
    url(r'^resetpwd/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', ResetpwdConfirmView.as_view(),name='resetpwd_confirm')
]

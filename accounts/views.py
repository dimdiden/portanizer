from django.shortcuts import redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)

from django.views.generic import FormView, View
from django.views.generic.edit import CreateView

from .forms import UserLoginForm, UserRegisterForm


User = get_user_model()


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(UserLoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return '/'


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "register.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        password = form.cleaned_data.get('password')
        self.object.set_password(password)
        self.object.save()
        new_user = authenticate(username=self.object.username, password=password)
        login(self.request, new_user)
        return super(UserRegisterView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

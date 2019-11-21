from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)

from django.db.models.query_utils import Q

from django.views.generic import FormView, View
from django.views.generic.edit import CreateView

from portanizer.settings import DEFAULT_FROM_EMAIL, ALLOWED_HOSTS


from .forms import (
    UserLoginForm,
    UserRegisterForm,
    PasswordResetRequestForm,
    SetPasswordForm
)

User = get_user_model()


class UserLoginView(FormView):
    form_class = UserLoginForm
    # template_name = "login.html"
    template_name = "auth_form.html"

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
    # template_name = "register.html"
    template_name = "auth_form.html"
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
        return redirect('authorization:login')


class ResetpwdView(FormView):
    # template_name = "resetpwd.html"
    template_name = "auth_form.html"
    success_url = '/authorization/login'
    form_class = PasswordResetRequestForm

    def get_context_data(self, **kwargs):
        context = super(ResetpwdView, self).get_context_data(**kwargs)
        context['title'] = 'Send me email'
        return context


    """
    This method here validates the if the input is an email address or not.
    Its return type is boolean, True if the input is a email address or False if its not.
    """
    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False


    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:

            associated_users = User.objects.filter(Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': ALLOWED_HOSTS[0],
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        subject_template_name = 'includes/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name = 'includes/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': ALLOWED_HOSTS[0],
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'includes/password_reset_subject.txt'
                    email_template_name = 'includes/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    # http://joequery.me/guides/python-smtp-authenticationerror/
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


class ResetpwdConfirmView(FormView):
    template_name = "auth_form.html"
    success_url = '/authorization/login'
    form_class = SetPasswordForm

    def get_context_data(self, **kwargs):
        context = super(ResetpwdConfirmView, self).get_context_data(**kwargs)
        context['title'] = 'Reset'
        return context

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):

        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)

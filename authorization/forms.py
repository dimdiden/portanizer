from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

# This method will return the currently active user model
# the custom user model if one is specified, or User otherwise.
User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter username'}), label='Username:')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password'}), label='Password:')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            user_auth = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user_auth:
                raise forms.ValidationError("Incorrect password")
            if not user_auth.is_active:
                raise forms.ValidationError("The user is no longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter username'}), label='Username:')
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter email'}), label='Email address:')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password'}), label='Password:')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter the same password'}), label='Confirm Password:')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'email',
        ]
# https://stackoverflow.com/questions/34609830/django-modelform-how-to-add-a-confirm-password-field
    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and len(password) <= 6:
            raise forms.ValidationError("Passwords must contain not less than 6 characters")
        if password != password2:
            raise forms.ValidationError("Passwords must match")

        return super(UserRegisterForm, self).clean(*args, **kwargs)


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter your email or username'}), label=("Email Or Username"))


class SetPasswordForm(forms.Form):

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'password_length': ("Passwords must contain not less than 6 characters"),
    }
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password'}), label='New password:')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter the same password'}), label='New password confirmation:')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if len(password) <= 6:
            raise forms.ValidationError(
                self.error_messages['password_length'],
                code='password_length',
            )

        if password and password2:
            if password != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

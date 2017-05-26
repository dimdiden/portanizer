from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

# This method will return the currently active user model
# the custom user model if one is specified, or User otherwise.
User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("The user is no longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username:')
    email = forms.EmailField(label='Email address:')
    # email2 = forms.EmailField(label='Confirm Email:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password:')

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

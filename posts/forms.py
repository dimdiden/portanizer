from django import forms
from .models import Tag, Post


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            "name": "New tag"
        }

    def __init__(self, user, *args, **kwargs):
        super(TagModelForm, self).__init__(*args, **kwargs)

        self.user = user

    def clean_name(self):
        if self.has_changed():
            data = self.cleaned_data['name']
            try:
                tag = Tag.objects.get(name=data, user=self.user)
            except Tag.DoesNotExist:
                tag = None
            if tag:
                raise forms.ValidationError(
                    "\"%s\" already exists for user %s" % (tag.name, self.user)
                )
            return data


class TagMultiplyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TagMultiplyForm, self).__init__(*args, **kwargs)

        self.fields['select_tag'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=Tag.objects.filter(user=user).order_by('name')
        )


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tag']

    def __init__(self, request, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        queryset = Tag.objects.filter(user=request.user)
        self.fields['tag'].queryset = queryset


def custom_tag_base_modelformset(user):
    class TagBaseModelFormSet(forms.BaseModelFormSet):

        def __init__(self, *args, **kwargs):
            self.user = user
            super(TagBaseModelFormSet, self).__init__(*args, **kwargs)

        # https://docs.djangoproject.com/en/1.11/topics/forms/formsets/#custom-formset-validation
        def clean(self):
            if any(self.errors):
                print(self.errors)
                return

            for form in self.forms:
                if form.has_changed():
                    data = form.cleaned_data['name']
                    try:
                        tag = Tag.objects.get(name=data, user=self.user)
                    except Tag.DoesNotExist:
                        tag = None
                    if tag:
                        form.add_error(
                            'name', "\"%s\" already exists for user %s" % (
                                tag.name, self.user))

    return TagBaseModelFormSet

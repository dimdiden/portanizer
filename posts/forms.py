from django import forms
from posts.models import Tag


# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(TagForm, self).__init__(*args, **kwargs)
#         self.fields["name"].queryset = Tag.objects.all()


class TagForm(forms.Form):
    select_tag = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all()
    )

    # def __init__(self, *args, **kwargs):
    #     super(TagForm, self).__init__(*args, **kwargs)
    #     self.fields["name"].widget = Tag.objects.all()
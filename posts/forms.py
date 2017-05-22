from django import forms
from posts.models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class TagMultiplyForm(forms.Form):
    select_tag = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all().order_by('name')
    )

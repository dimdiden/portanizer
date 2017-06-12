from django import forms
from django.forms import BaseModelFormSet
from .models import Tag


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        labels = {
            "name": "New tag"
        }

    # def clean(self):
    #     if 'tag_submit' in self.data:
    #         cleaned_data = super(TagModelForm, self).clean()
    #         print(self.data)
    #     else:
    #         print('NO')


class TagMultiplyForm(forms.Form):
    select_tag = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all().order_by('name')
    )


# class PostModelForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = '__all__'

    # def form_valid(self, form):
    #     messages.info(self.request, 'Success!!!!')
    #     return super(PostModelForm, self).form_valid(form)


class BaseTagFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseTagFormSet, self).__init__(*args, **kwargs)
        self.queryset = Tag.objects.all().order_by('-name')
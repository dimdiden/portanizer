from django.shortcuts import render
# from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from posts.models import Post, Tag
from posts.forms import TagForm


"""
Django: Search form in Class Based ListView
http://stackoverflow.com/questions/13416502/django-search-form-in-class-based-listview
"""


class PostListView(ListView):
    model = Post
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        """
        How to check for a POST method in a ListView in Django views?
        http://stackoverflow.com/questions/33876790/how-to-check-for-a-post-method-in-a-listview-in-django-views-im-getting-a-405
        """
        posts = self.get_queryset()
        if request.GET.getlist('select_tag'):
            tags = request.GET.getlist('select_tag')
            posts = Post.objects.filter(tag__in=tags).distinct()
        return render(request, self.template_name, {
            'posts': posts,
            'form': TagForm,
        })

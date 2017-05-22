from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
# from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from posts.models import Post, Tag
from posts.forms import TagMultiplyForm, TagForm


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
            'form': TagMultiplyForm(),
        })


class CreatePostView(CreateView):
    model = Post
    fields = '__all__'
    template_name = 'post.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        context['formTag'] = TagForm()
        return context


class UpdatePostView(UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'post.html'
    success_url = '/'

    """
    To do: implement post method which save Tag or Post
    """

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        context['formTag'] = TagForm()
        return context


class CreateTagView(CreateView):
    model = Tag
    fields = '__all__'
    template_name = 'post.html'
    success_url = '/'

    # def get_success_url(self):
    #     return redirect(self.request.META.get('HTTP_REFERER'))


class DeletePostView(DeleteView):
    model = Post
    template_name = 'confirm_delete.html'
    success_url = '/'


from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from posts.models import Post, Tag
from posts.forms import TagMultiplyForm, TagModelForm, PostModelForm


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
            'formMultyTag': TagMultiplyForm(),
        })


class CreatePostFormView(CreateView):
    model = Post
    fields = '__all__'
    template_name = 'post.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreatePostFormView, self).get_context_data(**kwargs)
        # context['form'] = PostModelForm()
        context['formNewTag'] = TagModelForm()
        context['formMultyTag'] = TagMultiplyForm()
        return context

    def post(self, request, *args, **kwargs):
        formPost = PostModelForm(request.POST)
        formTag = TagModelForm(request.POST)

        """
        Check if New tag form is valid or not.
        Redisplay the entered Post data.
        https://stackoverflow.com/questions/569468/django-multiple-models-in-one-template-using-forms
        """
        if formTag.is_valid():
            formTag.save()
            # return render_to_response(self.get_context_data(form=formPost))
            return render(request, 'post.html', {
                'formNewTag': TagModelForm(),
                'formMultyTag': TagMultiplyForm(),
                'form': formPost,
            })
        elif request.POST.get('name'):
            return render(request, 'post.html', {
                'formNewTag': formTag,
                'formMultyTag': TagMultiplyForm(),
                'form': formPost,
            })

        # Return the standard post method if the New tag is not specified 
        return super(CreatePostFormView, self).post(self, request, *args, **kwargs)


class UpdatePostFormView(UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'post.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UpdatePostFormView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        # context['form'] = PostModelForm()
        context['formNewTag'] = TagModelForm()
        context['formMultyTag'] = TagMultiplyForm()
        return context

    def post(self, request, *args, **kwargs):
        obj = Post.objects.get(pk=kwargs['pk'])
        formPost = PostModelForm(request.POST, instance=obj)
        formTag = TagModelForm(request.POST)

        # print(formTag.is_valid(), formPost.is_valid())
        if formTag.is_valid():
            formTag.save()
            return render(request, 'post.html', {
                'formMultyTag': TagMultiplyForm(),
                'formNewTag': TagModelForm(),
                'form': formPost,
            })
        elif request.POST.get('name'):
            return render(request, 'post.html', {
                'formMultyTag': TagMultiplyForm(),
                'formNewTag': formTag,
                'form': formPost,
            })

        # Return the standard post method if the New tag is not specified 
        return super(UpdatePostFormView, self).post(self, request, *args, **kwargs)


class CreateTagView(CreateView):
    model = Tag
    fields = '__all__'
    template_name = 'post.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreateTagView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        context['formNewTag'] = context.pop('form')
        context['formMultyTag'] = TagMultiplyForm()
        context['form'] = PostModelForm()
        print(context)
        return context


class DeletePostView(DeleteView):
    model = Post
    template_name = 'confirm_delete.html'
    success_url = '/'

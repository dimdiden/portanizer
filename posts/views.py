from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from posts.models import Post, Tag
from posts.forms import TagMultiplyForm, TagModelForm, PostModelForm
from django.contrib.auth.mixins import LoginRequiredMixin


"""
Django: Search form in Class Based ListView
http://stackoverflow.com/questions/13416502/django-search-form-in-class-based-listview
"""


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        """
        How to check for a POST method in a ListView in Django views?
        http://stackoverflow.com/questions/33876790/how-to-check-for-a-post-method-in-a-listview-in-django-views-im-getting-a-405
        """
        posts = self.get_queryset()
        if request.path == '/unassigned/':
            posts = Post.objects.filter(tag__isnull=True).distinct()
        elif request.GET.getlist('select_tag'):
            tags = request.GET.getlist('select_tag')
            posts = Post.objects.filter(tag__in=tags).distinct()     
        return render(request, self.template_name, {
            'posts': posts,
            'formMultyTag': TagMultiplyForm(),
        })

        # def get_queryset(self):
        #     """
        #     If an extra key is passed(url), the specific page is displayed.
        #     """
        #     if 'extra' in self.kwargs and self.kwargs['extra'] == 'last_24_hours':
        #         last_24_hours = datetime.today() - timedelta(days=1)
        #         return Product.objects.all().filter(created_at__gte=last_24_hours)
        #     else:
        #         return Product.objects.all().filter(
        #             category=Category.objects.get(slug=self.kwargs['category_slug']))


class CreatePostFormView(LoginRequiredMixin, CreateView):
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


class UpdatePostFormView(LoginRequiredMixin, UpdateView):
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


# class CreateTagView(CreateView):
#     model = Tag
#     fields = '__all__'
#     template_name = 'post.html'
#     success_url = '/'

#     def get_context_data(self, **kwargs):
#         context = super(CreateTagView, self).get_context_data(**kwargs)
#         context.update(self.kwargs)
#         context['formNewTag'] = context.pop('form')
#         context['formMultyTag'] = TagMultiplyForm()
#         context['form'] = PostModelForm()
#         print(context)
#         return context


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'confirm_delete.html'
    success_url = '/'


class UpdateTagFormView(LoginRequiredMixin, TemplateView):
    template_name = 'tag_manager.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateTagFormView, self).get_context_data(**kwargs)
        context['formMultyTag'] = TagMultiplyForm()
        if 'formNewTag' in kwargs:
            context['formNewTag'] = kwargs['formNewTag']
        else:
            context['formNewTag'] = TagModelForm()
        context['forms'] = []
        if 'tag' and 'formUpdTag' in kwargs:
            queryset = Tag.objects.exclude(id=kwargs['tag'].id).order_by('name')
            print(queryset)
            formset = [kwargs['formUpdTag'], kwargs['tag'].id]
            context['forms'].append(formset)
            for tag in queryset:
                formset = [TagModelForm(instance=tag), tag.id]
                context['forms'].append(formset)
        else:
            queryset = Tag.objects.all().order_by('name')
            for tag in queryset:
                formset = [TagModelForm(instance=tag), tag.id]
                context['forms'].append(formset)

        return context

    def post(self, request, *args, **kwargs):
        # obj = Post.objects.get(pk=kwargs['pk'])
        # formPost = PostModelForm(request.POST, instance=obj)
        if 'pk' in kwargs:
            obj = Tag.objects.get(pk=kwargs['pk'])
            formTag = TagModelForm(request.POST, instance=obj)
            if formTag.is_valid():
                formTag.save()
                return redirect('tagmanager')
            else:
                print('WRONG')
                return render(request, 'tag_manager.html', self.get_context_data(formUpdTag=formTag, tag=obj))
            return redirect('/')
        else:
            # print(kwargs)
            formTag = TagModelForm(request.POST)

            print(formTag.is_valid())
            if formTag.is_valid():
                formTag.save()
                return redirect('tagmanager')
            else:
                return render(request, 'tag_manager.html', self.get_context_data(formNewTag=formTag))

# https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
# http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/


class DeleteTagView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'confirm_delete.html'
    success_url = '/tagmanager'

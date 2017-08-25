import math

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Count
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .models import Post, Tag
from .forms import TagModelForm, PostModelForm, custom_tag_base_modelformset


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)

        tags = self.request.GET.getlist('select_tag')
        condition = self.request.GET.get('condition')
        unassigned = self.request.GET.get('show_unassigned')

        # do not use unassigned when condition and tags are present
        if condition and tags:
            unassigned = None

        if unassigned and tags:
            return queryset.filter(
                Q(tag__isnull=True) | Q(tag__in=tags)).distinct()
        elif unassigned:
            return queryset.filter(tag__isnull=True)
        elif tags:
            if condition:
                # return posts which include all tags
                return queryset.filter(tag__in=tags).annotate(
                    matched_tags=Count('tag')).filter(matched_tags=len(tags))

            # return posts matched any of tags
            return queryset.filter(tag__in=tags).distinct()
        return queryset


class CreatePostFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'post.html'
    success_url = '/posts/'
    success_message = "%(title)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super(CreatePostFormView, self).get_context_data(**kwargs)

        context['formNewTag'] = TagModelForm(self.request.user)

        # if formNewTag in kwargs - replace existed
        context.update(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        # to overcome the issue has no attribute 'object'
        self.object = None

        formTag = TagModelForm(request.user, request.POST)

        # Separate processes for two forms based on name html attribute
        if 'tag_submit' in request.POST:
            if formTag.is_valid():
                new_tag = formTag.save(commit=False)
                new_tag.user = self.request.user
                new_tag.save()

                return render(
                    request,
                    self.template_name,
                    self.get_context_data())
            else:
                return render(
                    request,
                    self.template_name,
                    self.get_context_data(formNewTag=formTag))

        # Return the standard post method if the New tag is not specified
        return super(
            CreatePostFormView, self).post(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreatePostFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        self.object = instance
        return super(CreatePostFormView, self).form_valid(form)


class UpdatePostFormView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'post.html'
    success_url = '/posts/'
    success_message = "%(title)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super(UpdatePostFormView, self).get_context_data(**kwargs)

        # to get the pk's
        context.update(self.kwargs)

        context['formNewTag'] = TagModelForm(self.request.user)

        # if formNewTag in kwargs - replace existed
        context.update(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        formTag = TagModelForm(request.user, request.POST)

        # Separate processes for two forms based on name html attribute
        if 'tag_submit' in request.POST:
            if formTag.is_valid():
                new_tag = formTag.save(commit=False)
                new_tag.user = self.request.user
                new_tag.save()

                return render(
                    request,
                    self.template_name,
                    self.get_context_data())
            else:
                return render(
                    request,
                    self.template_name,
                    self.get_context_data(formNewTag=formTag))

        # Return the standard post method if the New tag is not specified
        return super(
            UpdatePostFormView, self).post(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdatePostFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        self.object = instance
        return super(UpdatePostFormView, self).form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'confirm_delete.html'
    success_url = '/'


class TagManagerView(LoginRequiredMixin, TemplateView):

    template_name = 'tag_manager.html'

    def get_context_data(self, **kwargs):
        context = super(TagManagerView, self).get_context_data(**kwargs)

        # gets formset from get and post methods
        context.update(kwargs)

        # delimeter for columns
        # -1 - extra form, then round to up value
        context['column_count'] = math.ceil(
            (kwargs['formset'].total_form_count() - 1) / 3)
        return context

    def get(self, request, *args, **kwargs):
        queryset = Tag.objects.filter(user=self.request.user).order_by('-name')

        formset = custom_tag_base_modelformset(request.user)

        # https://djangosnippets.org/snippets/2552/
        # https://stackoverflow.com/questions/622982/django-passing-custom-form-parameters-to-formset/25766319#25766319
        TagFormSet = modelformset_factory(
            Tag,
            formset=formset,
            fields=('name',),
            can_delete=True)

        formset = TagFormSet(queryset=queryset)
        return self.render_to_response(self.get_context_data(
            formset=formset))

    def post(self, request, *args, **kwargs):
        # https://stackoverflow.com/questions/34214547/modifying-a-inline-formset-before-it-is-saved

        formset = custom_tag_base_modelformset(request.user)

        TagFormSet = modelformset_factory(
            Tag,
            formset=formset,
            fields=('name',),
            can_delete=True)

        formset = TagFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = self.request.user
                # you’ll also need to call formset.save_m2m()
                # to ensure the many-to-many relationships are saved properly.
                instance.save()

            for instance in formset.deleted_objects:
                instance.delete()
            return redirect('posts:tagmanager')
        else:
            return self.render_to_response(self.get_context_data(
                formset=formset))

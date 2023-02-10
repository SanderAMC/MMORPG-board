from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .filters import CommentFilter
from django.contrib.auth.models import User
from .forms import UserForm, PostForm
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.urls import reverse_lazy

class PostList(ListView):
    model = Post
    ordering = '-creation'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user

        comment_list = []
        for obj in context['post_list']:
            obj = model_to_dict(obj, fields=['id', 'author', 'creation', 'category', 'title', 'content'])
            if Comment.objects.order_by('-creation').filter(post=obj['id']).exists():
                obj['last_comment'] = Comment.objects.order_by('-creation').filter(post=obj['id'])[0].text
                obj['last_comment_author'] = Comment.objects.order_by('-creation').filter(post=obj['id'])[0].user
            else:
                obj['last_comment'] = 'Пока нет комментариев'

            obj['category'] = [_[1] for _ in Post.TYPES if _[0] == obj['category']][0]
            comment_list.append(obj)

        context['post_list'] = comment_list

        return context


class CommentListFiltered(ListView):
    model = Comment
    ordering = '-creation'
    template_name = 'comment_list.html'
    context_object_name = 'comment_flist'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user

        return context

    def get_queryset(self):
        posts = Post.objects.filter(author=self.request.user)

        for post in posts:
            print(post)
        queryset = Comment.objects.order_by('-creation').filter(post=3)
        print(queryset)
        self.filterset = CommentFilter(self.request.GET, queryset)
        print(self.filterset)
        return self.filterset.qs


class UserView(TemplateView):
    template_name = 'user_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context

class UserUpdate(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'user_edit.html'
    def form_valid(self, form):
        self.success_url = '/user/'
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) \
            if self.get_object().id == request.user.id else HttpResponse(status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context

class OnePost(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'one_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    # permission_required = ('news.add_post', )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        self.success_url = reverse_lazy('post_list')
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user
        return context

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context

    def form_valid(self, form):
        # self.success_url = reverse('one_post', args=[str(self.id)])
        self.success_url = reverse_lazy('post_list')
        return super().form_valid(form)

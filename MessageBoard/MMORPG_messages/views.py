from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import NewsFilter

# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-creation'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_list = []
        for obj in context['object_list']:
            if Comment.objects.order_by('-creation').filter(post=obj.id).exists():
                comment_list.append(Comment.objects.order_by('-creation').filter(post=obj.id)[0].text)
            else:
                comment_list.append('Пока нет комментариев')

            context['comment_list'] = comment_list
        print(context)
        return context

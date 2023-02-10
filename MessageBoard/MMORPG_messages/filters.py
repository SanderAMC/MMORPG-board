from django_filters import *
import django_filters
from .models import Comment
from django import forms


class CommentFilter(FilterSet):
    # category = django_filters.ChoiceFilter(choices=[[c.id, c.name] for c in Category.objects.all().order_by('name')],
    #                                        label="Категория новости ")
    # post_type = django_filters.ChoiceFilter(choices=Post.TYPES, label="Тип поста ", lookup_expr='iexact')
    creation = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                                          label="Создано позднее, чем ", lookup_expr='date__gt')
    #approved = django_filters.ChoiceFilter(choices=Post.TYPES, label="Тип поста ", lookup_expr='iexact')

    class Meta:
       model = Comment
       fields = {
           # 'title': ['icontains'],
       }




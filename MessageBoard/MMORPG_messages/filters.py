from django_filters import *
import django_filters
from .models import Comment, Post
from django import forms

class CommentFilter(FilterSet):
    post = django_filters.ChoiceFilter(choices=lambda: [(p.id, f'{p.id} - {p.title} - {p.creation.strftime("%d-%m-%Y %H:%M")}')
                                                        for p in Post.objects.all().order_by('-creation')], label="Сообщение:")
    creation = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                                         label="Создано позднее, чем ", lookup_expr='date__gt')
    approved = django_filters.ChoiceFilter(choices=[('0', 'Нет'), ('1', 'Да')], label="Согласован:", lookup_expr='iexact')

    class Meta:
        model = Comment
        fields = {
            # 'approved',
        }



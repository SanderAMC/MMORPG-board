from django_filters import *
import django_filters
from .models import Comment, Post
from django import forms
from datetime import datetime
from typing import Callable
from django_filters.conf import settings

class MMORPGChoiceFilter(django_filters.ChoiceFilter):
    def get_field_choices(self):
        choices = self.extra.get('choices', [])
        if isinstance(choices, Callable):
            choices = choices()
        return choices

    @property
    def field(self):
        if not hasattr(self, '_field'):
            field_kwargs = self.extra.copy()
            if settings.DISABLE_HELP_TEXT:
                field_kwargs.pop('help_text', None)

            field_kwargs.update(choices=self.get_field_choices())
            self._field = self.field_class(label=self.label, **field_kwargs)
        return self._field


class CommentFilter(FilterSet):
    post = MMORPGChoiceFilter(choices=lambda: [(p.id, f'{p.id} - {p.title} - {p.creation.strftime("%d-%m-%Y %H:%M")}')
                                                for p in Post.objects.all().order_by('-creation')], label="Сообщение:")
    creation = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                                          label="Создано позднее, чем ", lookup_expr='date__gt')
    approved = django_filters.ChoiceFilter(choices=[('0', 'Нет'), ('1', 'Да')], label="Согласован", lookup_expr='iexact')

    class Meta:
       model = Comment
       fields = {
           # 'approved',
       }




from django.urls import path
# Импортируем созданное нами представление
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('<int:pk>', OnePost.as_view(), name='one_post'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
]
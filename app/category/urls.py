from django.urls import path

from .views import CategoryViewSetAPI

app_name = 'category'

urlpatterns = [
    path('list/', CategoryViewSetAPI.as_view({'get': 'list'}),
         name='category-list'),
    path('create/', CategoryViewSetAPI.as_view({'post': 'create'}),
         name='category-create')
]

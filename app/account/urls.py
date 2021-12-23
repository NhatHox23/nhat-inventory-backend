from django.urls import path
from .views import UserViewSetApi

app_name = 'account'

urlpatterns = [
    path('list-user/', UserViewSetApi.as_view({'get': 'list'}),
         name='list-user'),
    path('create/', UserViewSetApi.as_view({'post': 'create'}),
         name='create-user')
]

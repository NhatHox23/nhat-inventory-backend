from django.urls import path
from .views import UserViewSetApi, VerifyEmail, UserSelfProfileApi

app_name = 'account'

urlpatterns = [
    path('list-user/', UserViewSetApi.as_view({'get': 'list'}),
         name='list-user'),
    path('create/', UserViewSetApi.as_view({'post': 'create'}),
         name='create-user'),
    path('email-verify/', VerifyEmail.as_view({'get': 'list'}),
         name='verify-email'),
    path('detail/', UserSelfProfileApi.as_view({'get': 'list',
                                                'patch': 'partial_update'}),
         name='detail-self-user')
]

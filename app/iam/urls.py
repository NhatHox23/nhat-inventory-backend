from django.urls import path
from .views import MyTokenObtainPairView, MyRefreshTokenObtainPairView, \
    PermissionViewSetApi, GroupViewSetApi

app_name = "iam"

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', MyRefreshTokenObtainPairView.as_view(),
         name="token_refresh"),
    path('permission/list/', PermissionViewSetApi.as_view({'get': 'list'}),
         name='permission_list'),
    path('group/list/', GroupViewSetApi.as_view({'get': 'list'}),
         name='group_list'),
    path('group/create/', GroupViewSetApi.as_view({'post': 'create'}),
         name='group_create')
]

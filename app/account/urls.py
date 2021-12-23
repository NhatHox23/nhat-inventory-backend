from django.urls import path
from .views import MyTokenObtainPairView, PermissionApiViewSets, \
    UserProfileApiViewSets, GroupApiViewSets

app_name = 'account'

urlpatterns = [
    path('log-in/', MyTokenObtainPairView.as_view(), name="log-in"),
    path('profile/', UserProfileApiViewSets.as_view({'get': 'list'}),
         name="list-profile"),
    path('permission/', PermissionApiViewSets.as_view({'get': 'list'}),
         name="list-permission"),
    path('group/list/', GroupApiViewSets.as_view({'get': 'list'}),
         name="list-group"),
    path('group/create/', GroupApiViewSets.as_view({'post': 'create'}),
         name="create-group"),
    path('group/<int:group_id>/add-permission/', GroupApiViewSets.as_view({
        'patch': 'update'}), name='add-permission-group')

]

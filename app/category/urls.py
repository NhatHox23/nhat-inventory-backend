from django.urls import path
from .views import CategoryApiViewSet

app_name = 'category'

urlpatterns = [
    path('list/', CategoryApiViewSet.as_view({'get': 'list'}),
         name="list-category")
]

from django.urls import path
from .views import ProductViewSetAPI

app_name = 'product'

urlpatterns = [
    path('list/', ProductViewSetAPI.as_view({'get': 'list'}),
         name='product-list'),
    path('create/', ProductViewSetAPI.as_view({'post': 'create'}),
         name='product-create'),
    path('put/<int:product_id>', ProductViewSetAPI.as_view({'put': 'update'}),
         name='product-put')
]
from django.urls import path
from .views import MyTokenObtainPairView

app_name = 'account'

urlpatterns = [
    path('log-in/', MyTokenObtainPairView.as_view(), name="log-in"),
]

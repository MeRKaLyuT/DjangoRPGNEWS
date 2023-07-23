from .views import SignUp
from django.urls import path, include

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
]
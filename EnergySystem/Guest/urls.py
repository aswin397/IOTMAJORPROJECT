from django.urls import path,include
from . import views


app_name="Guest"

urlpatterns = [
    path('', views.home, name='home'),
    path('Login', views.Login, name='Login'),
]
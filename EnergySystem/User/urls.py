from django.urls import path,include
from . import views


app_name="User"

urlpatterns = [
path('home', views.home, name='home'),
path('myprofile', views.myprofile, name='myprofile'),
path('feedback', views.feedback, name='feedback'),
path('bills', views.bills, name='bills'),
path('bills2/<int:id>/', views.bills2, name='bills2'),
path('payments', views.payments, name='payments'),
path('get-electricity-usage', views.getelectricityusage, name='get-electricity-usage'),
path('get-electricity-usage2', views.getelectricityusage2, name='get-electricity-usage2'),
]
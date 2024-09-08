from django.urls import path,include
from . import views


app_name="Admin"

urlpatterns = [
path('home', views.home, name='home'),
path('Addoffice',views.Addoffice,name="Addoffice"),
path('viewoffice',views.viewoffice,name="viewoffice"),
path('Viewusers',views.Viewusers,name="Viewusers"),
path('Payments',views.Payments,name="Payments"),
path('Feedback',views.Feedback1,name="Feedback")
]
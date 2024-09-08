from django.urls import path,include
from . import views


app_name="KSEB"

urlpatterns = [
path('home', views.home, name='home'),
path('addconsumers', views.addconsumers, name='addconsumers'),
path('viewconsumers', views.viewconsumers, name='viewconsumers'),
path('edit_consumer/<int:consumer_id>/', views.edit_consumer, name='edit_consumer'),
path('block_consumer/<int:consumer_id>/', views.block_consumer, name='block_consumer'),
path('Feedback', views.Feedback1, name='Feedback'),
path('ANNOUNCEMENT', views.ANNOUNCEMENT, name='ANNOUNCEMENT'),
path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
path('Payments', views.Payments, name='Payments'),
path('Usage', views.Usage, name='Usage'),
path('view_more/<int:consumer_id>/', views.view_more, name='view_more'),
path('GenerateBill/<int:consumer_id>/', views.GenerateBill, name='GenerateBill')

]
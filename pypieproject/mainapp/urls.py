from django.urls import path     
from . import views

urlpatterns = [ 
    path('', views.index),
    path('dashboard' , views.display_dashboard)  ,
    path('createpie' , views.create_pie),
    path('createuserform' , views.create_user_form),
    path('createpieform' , views.create_pie_form),    
    path('updatepieform' , views.update_pie_form),      
    path('logout' , views.logout_form)
    ]
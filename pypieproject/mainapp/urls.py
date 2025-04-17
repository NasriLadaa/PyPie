from django.urls import path     
from . import views

urlpatterns = [ 
    path('', views.index),
    path('dashboard' , views.display_dashboard)  ,
    path('createpie' , views.create_pie),
    path('createuserform' , views.create_user_form),
    path('createpieform' , views.create_pie_form),  
    path('editpie/<int:id>' , views.update_pie),   
    path('viewpie/<int:id>' , views.view_pie),   
    path('updatepieform' , views.update_pie_form),   
    path('loginuserform' , views.login_user_form), 
    path('vote_pie_form' , views.vote_pie_form)  ,
    path('logout' , views.logout_form)
    ]
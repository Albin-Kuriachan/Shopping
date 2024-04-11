
from django.urls import path
from account import views

urlpatterns = [

    path('signin/', views.signin,name='signin'),
    path('signup/', views.signup,name='signup'),
    path('logoutfun/', views.logoutfun, name='logoutfun'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('rest_password/', views.rest_password, name='rest_password'),
    path('change_password/<token>/',views. change_password, name="change_password"),

]
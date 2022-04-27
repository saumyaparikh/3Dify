from django.urls import path
from . import views
from django.http import request
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name="signup"),
    path('loginuser',views.loginuser,name="loginuser"),  
    path('logoutuser',views.logoutuser,name="logoutuser"),
    path('download',views.download,name="download"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('download2',views.download2,name="download2"),
    path('aboutus',views.aboutus,name="aboutus"),
]

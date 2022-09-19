from re import template
from django.urls import path
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, PasswordChangeDoneView
from . import views

urlpatterns = [
    path('signup', views.handlesignup, name='signup'),
    path("send_otp",views.send_otp,name="send otp"),
    path('login',views.login, name='login'),
    path('forget-pass',views.forget_pass, name='forget-pass'),
    path('send-reset-otp',views.send_reset_pass_otp, name='send-reset-otp'),
    path('resend-otp',views.resend_otp, name='resend-otp'),
    path('confirm-otp',views.confirm_otp, name='confirm-otp'),
    path('pass-confirm',views.confirm_pass, name='pass-confirm'),
    path('',views.home, name='index'),
    path('home',views.index, name='homepage'),
    path('about',views.about_us, name='aboutus'),
    path('contact',views.contact_us, name='contactus'),
    path('auth-logout-basic.html', views.logout, name='logout'),
    # path('/data', views.dataa, name='index'),
    #  path('t/', views.testing, name='index'),1
    # path('products/<int:id>', views.viewpara, name = 'view_products')
]

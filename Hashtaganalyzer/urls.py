from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.handlesignup, name='signup'),
    path("send_otp",views.send_otp,name="send otp"),
    path('login',views.login, name='login'),
    path('',views.home, name='index'),
    path('home',views.index, name='homepage'),    
    path('about',views.about_us, name='aboutus'),
    path('contact',views.contact_us, name='contactus'),            
    path('auth-logout-basic.html', views.logout, name='logout')
    # path('/data', views.dataa, name='index'),
    #  path('t/', views.testing, name='index'),1
    # path('products/<int:id>', views.viewpara, name = 'view_products')
]

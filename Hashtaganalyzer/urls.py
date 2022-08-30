from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='index'),
    path('about',views.about_us, name='aboutus'),
    path('home',views.index, name='homepage'),
    path('login',views.login, name='login'),
    path('signup', views.handlesignup, name='signupapi'),
    path('auth-logout-basic.html', views.logout, name='logout')
    # path('/data', views.dataa, name='index'),
    #  path('t/', views.testing, name='index'),1
    # path('products/<int:id>', views.viewpara, name = 'view_products')
]

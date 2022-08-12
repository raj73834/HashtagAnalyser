from django.urls import path
from . import views

urlpatterns = [
    path('home',views.index, name='homepage'),
    path('login',views.signin, name='login'),
    path('', views.handlesignup, name='signupapi'),
    # path('/data', views.dataa, name='index'),
    #  path('t/', views.testing, name='index'),1
    # path('products/<int:id>', views.viewpara, name = 'view_products')
]

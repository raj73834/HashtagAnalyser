from django.urls import path
from . import views

urlpatterns = [
    path('auth-signup-basic.html',views.signup, name='register'),
    path('auth-signin-basic.html',views.signin, name='login'),
    path('dashboard-crm.html', views.index, name='index'),
    # path('/data', views.dataa, name='index'),
    #  path('t/', views.testing, name='index'),1
    # path('products/<int:id>', views.viewpara, name = 'view_products')
]

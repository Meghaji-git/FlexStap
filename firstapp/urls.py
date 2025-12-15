"""
URL configuration for firstproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('cart', views.cart, name='cart'),
    path('couponCode', views.couponCode, name='couponCode'),
    path('addCart<int:sp>', views.addCart, name='addCart'),
    path('decreaseCart<int:sp>', views.decreaseCart, name='decreaseCart'),
    path('addToCart<int:sp>', views.addToCart, name='addToCart'),
    path('delete<int:sp>',views.delete, name='delete'),

    path('category', views.category, name='category'),
    # path('single_product', views.single_product, name='single_product'),
    path('single_product<int:sp>', views.single_product, name='single_product'),
    path('wish_list1<int:pi>',views.wish_list1, name='wish_list1'),
    path('wish_list',views.wish_list, name='wish_list'),
    path('list_delete<int:did>',views.list_delete, name='list_delete'),
    
    path('checkout', views.checkout, name='checkout'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('elements', views.elements, name='elements'),
    path('order', views.order, name='order'),

    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('confirm_password', views.confirm_password, name='confirm_password'),

    path('single_blog', views.single_blog, name='single_blog'),
    
    path('tracking', views.tracking, name='tracking'),
    path('contact', views.contact, name='contact'),
    
    
]

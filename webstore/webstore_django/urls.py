from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:id>', views.product, name='product'),
    path('product_list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('search_product/<slug:search_parameters>', views.search_product),
    path('add_shopping_cart/', views.add_shopping_cart),
    path('remove_shopping_cart', views.remove_shopping_cart),
    path('get_shopping_cart', views.get_shopping_cart),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]

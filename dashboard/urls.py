from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('sales/', views.sales_analytics, name='sales_analytics'),
    path('products/', views.product_management, name='product_management'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('orders/', views.order_management, name='order_management'),
    path('api/stats/', views.api_dashboard_stats, name='api_stats'),
]


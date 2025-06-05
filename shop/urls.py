from django.urls import path
from . import views

urlpatterns = [
	path('', views.landing_page, name='landing_page'),
	path('products/', views.product_list, name='product_list'),
	path('product/<int:pk>/', views.product_detail, name='product_detail'),
	path('order/<int:pk>/', views.place_order, name='place_order'),
	path('orders/', views.order_history, name='order_history'),
	path('cart/', views.view_cart, name='view_cart'),
	path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
	path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
	path('cart/checkout/', views.checkout, name='checkout'),
	path('cart/count/', views.get_cart_count, name='get_cart_count'),
	path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
]

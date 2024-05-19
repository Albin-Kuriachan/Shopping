
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index,name='index'),
    # path('apply_candidate_profile/<int:pk>/', views.apply_candidate_profile, name='apply_candidate_profile'),
    path('base/', views.base, name='base'),
    # path('single_product/<int:pk>/', views.single_product, name='single_product'),
    path('single_product/<int:pk>/<int:pid>/', views.single_product, name='single_product'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('category/<int:id>/', views.category, name='category'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_id>/<int:quantity_id>/', views.add_cart, name='add_cart'),
    path('substrate_cart/<int:product_id>/<int:quantity_id>/', views.substrate_cart, name='substrate_cart'),
    path('remove_from_cart/<int:product_id>/<int:quantity_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('select_address/', views.select_address, name='select_address'),
    path('add_address/', views.add_address, name='add_address'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('delete_payment/<int:id>/', views.delete_payment, name='delete_payment'),
    path('order_preview/', views.order_preview, name='order_preview'),
    path('place_order/<int:address_id>/', views.place_order, name='place_order'),
    path('set_as_default/<int:address_id>/', views.set_as_default, name='set_as_default'),
    path('order_view/', views.order_view, name='order_view'),
    path('filter/', views.filter, name='filter'),
    path('low_to_high/', views.low_to_high, name='low_to_high'),
    path('high_to_low/', views.high_to_low, name='high_to_low'),

]
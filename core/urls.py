from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('menu/<str:tag>/', views.menu, name='menu_with_tag'),
    path('menu-detail/<uuid:pk>/', views.menu_detail, name='menu_detail'),
    path('contact/', views.contact, name='contact'),
    path('sentmail/', views.send_purchase_receipt_email,
         name='send_purchase_receipt_email'),
    path('cart/', views.cart, name='cart'),
    path('cart-add/<uuid:meal_id>/',
         views.cartAdd, name='cart_add'),
    path('cart-remove/<uuid:cart_item_id>/',
         views.cartRemove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('order-created/<int:totalPrice>/',
         views.create_order, name='create_order'),
    path('order-created/', views.create_shipping_address,
         name='create_order_no_total'),
    path('shipping-address/', views.create_shipping_address,
         name='shipping_address'),


    path('shipping/', views.shipping_address,
         name='shipping'),

]

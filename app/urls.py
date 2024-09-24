from django.urls import path

from .views import *

#no app name

urlpatterns = [
    path('', index, name="index-page"),
    path('checkout/', checkout, name="checkout-page"),
    # path('signup/',signup,name="signup-page"),
    # path('login/',login,name="login-page"),
    path('shop/', Shop, name="shop-page"),
    path('shop-details/<int:product_id>/', ShopDetails, name="shopdetails-page"),
    path('contact/', Contact, name="contact-page"),
    # path('logout/',logout,name="logout-function"),
    path('Adminlogin/', Adminlogin, name="adminlogin-page"),
    path('Adminlogout/', Adminlogout, name="adminlogout-function"),
    # For Cart functionlity url
    path('cart/', cart_view, name='cart'),
    path('shop-details/<int:Product_id>/cart/', add_to_cart, name="add_to_cart"),
    path('cart/update/<int:cart_item_id>/<str:action>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart')

]

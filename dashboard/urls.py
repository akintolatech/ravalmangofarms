from django.urls import path
from .views import *


app_name = 'dashboard'

urlpatterns = [
    path('',index,name="dashboard"),
    path('delete-user/<int:user_id>/',delete_user,name="delete-user"),
    path('add-products/',add_product,name="add-product"),
    path('show-products/',show_products,name="all-products"),
    path('products/<int:pk>/delete/',delete_product, name='delete_product'),
    path('products/<int:pk>/edit/',edit_product, name='edit-product'),


    path('all-featureProducts/',AllFeatureProducts, name='feature-product'),
    path('featured-products/<int:pk>/delete/',delete_featured_product, name='delete_product'),
    path('featured-products/<int:pk>/edit/',edit_featured_product, name='edit_product'),
    path('add-feature-product/',add_featured_product, name='add_product'),
    path('best_products/',best_products, name='best_product'),
    path('best_products/<int:best_id>/delete/',delete_best_products, name='delete_best_product'),
    path('add_best_product/',add_best_products, name='add_best_product'),


    path('all-category/',all_category, name='all_category'),
    path('all-category/<int:category_id>/delete/',delete_category, name='delete_category'),
    path('add-category/',add_category,name="add-category"),
    path('customer-profile/<int:customer_id>/',customer_data,name="customer-profile")












]






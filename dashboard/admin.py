from django.contrib import admin
from .models import *

# Register your models here.

# @admin.register(Signup)
# class SignupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email')
#     search_fields = ('name', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'created_at', 'updated_at')
    ordering = ('-created_at',)



@admin.register(KG)
class KGAdmin(admin.ModelAdmin):
    list_display = ('name','price')




@admin.register(FeaturedProduct)
class FeaturedAdmin(admin.ModelAdmin):
    list_display = ('product','disount_price')



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price')


@admin.register(BestProducts)
class BestProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'products_name', 'products_price')

    def products_name(self, obj):
        return obj.products.name
    products_name.short_description = 'Product Name'

    def products_price(self, obj):
        return obj.products.price
    products_price.short_description = 'Product Price'




@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 
        'last_name', 
        'company_name', 
        'city', 
        'country', 
        'postcode', 
        'mobile', 
        'email'
    )
    search_fields = (
        'first_name', 
        'last_name', 
        'company_name', 
        'email'
    )
    list_filter = ('city', 'country')


@admin.register(FinalProduct)
class FinalProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'quantity', 'total_price','final_price','uploaded_file', 'user_profile_email')

    def user_profile_email(self, obj):
        return obj.user_profile.email
    user_profile_email.short_description = 'User Email'





from django.db import models
from decimal import Decimal
# Create your models here.



# class Signup(models.Model):
#     name = models.CharField(max_length=255,default='')
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255,default='')


#     def __str__(self):
#             return self.name




class KG(models.Model):
    name = models.CharField(max_length=200, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)




    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name





class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    kg = models.ForeignKey(KG,on_delete=models.CASCADE,blank=True,null=True)
    file = models.FileField(upload_to='Products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = self.name if self.name else "No name"
        category_name = self.category.name if self.category else "No category"
        price = str(self.price) if self.price is not None else "No price"
        return f"{name} /{category_name}/ {price}"




class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    disount_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)





class CartItem(models.Model):
    # user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.price * Decimal(self.quantity)





class BestProducts(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.products)







class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    file = models.FileField(upload_to='user_files/', blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.first_name





class FinalProduct(models.Model):
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,default='')
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    uploaded_file = models.FileField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.product_name}"




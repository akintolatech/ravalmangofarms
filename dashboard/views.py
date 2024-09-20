from django.shortcuts import render, redirect,get_object_or_404
from .models import *
# Create your views here.


def index(request):
    user_profiles = UserProfile.objects.all()

    email_to_products = []
    for profile in user_profiles:
        email = profile.email
        profile_id = profile.id
        products = FinalProduct.objects.filter(user_profile=profile)  # Adjust the filter according to your model's relation
        email_to_products.append({
            'email': email,
            'profile_id': profile_id,
            'products': products
        })

    context = {
        'email_to_products': email_to_products,
    }

    return render(request, 'dashboard/index.html', context)




def customer_data(request, customer_id):
    user_profile = get_object_or_404(UserProfile, id=customer_id)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'dashboard/order_user_profile.html', context)






def delete_user(request,user_id):


    user = get_object_or_404(Signup, id=user_id)
    
    # Delete the user
    user.delete()

    return redirect('dashboard:dashboard')


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        kg_id = request.POST.get('kg')
        file = request.FILES.get('file')

        category = Category.objects.get(id=category_id) if category_id else None
        kg = KG.objects.get(id=kg_id) if kg_id else None

        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            kg=kg,
            file=file
        )
        product.save()

        return redirect('dashboard:all-products')

    categories = Category.objects.all()
    kgs = KG.objects.all()
    return render(request, 'dashboard/add_products.html', {'categories': categories, 'kgs': kgs})


def show_products(request):
    products = Product.objects.all()
    return render(request, 'dashboard/product_list.html', {'products': products})





def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('dashboard:all-products')


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category_id = request.POST.get('category')
        product.kg_id = request.POST.get('kg')
        if request.FILES.get('file'):
            product.file = request.FILES.get('file')
        product.save()
        return redirect('dashboard:all-products')
    categories = Category.objects.all()
    kgs = KG.objects.all()
    return render(request, 'dashboard/edit_product.html', {'product': product, 'categories': categories, 'kgs': kgs})



def AllFeatureProducts(request):
    featured_products = FeaturedProduct.objects.all()
    return render(request, 'dashboard/AllFeatureProducts.html', {'featured_products': featured_products})


def delete_featured_product(request, pk):
    featured_product = get_object_or_404(FeaturedProduct, pk=pk)
    featured_product.delete()
    return redirect('dashboard:feature-product')



def edit_featured_product(request, pk):
    featured_product = get_object_or_404(FeaturedProduct, pk=pk)
    if request.method == 'POST':
        featured_product.disount_price = request.POST.get('discount_price')
        featured_product.product_id = request.POST.get('product')
        featured_product.save()
        return redirect('dashboard:feature-product')
    products = Product.objects.all()
    return render(request, 'dashboard/edit_featured_product.html', {'featured_product': featured_product, 'products': products})



def add_featured_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        discount_price = request.POST.get('discount_price')
        product = get_object_or_404(Product, id=product_id)
        FeaturedProduct.objects.create(product=product, disount_price=discount_price)
        return redirect('dashboard:feature-product')
    
    products = Product.objects.all()
    return render(request, 'dashboard/add_featured_product.html', {'products': products})




def best_products(request):
    best_products = BestProducts.objects.all()
    return render(request, 'dashboard/BestProducts.html', {'best_products': best_products})


def delete_best_products(request, best_id):
    product = get_object_or_404(BestProducts, pk=best_id)
    product.delete()
    return redirect('dashboard:best_product')



def add_best_products(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                best_product = BestProducts.objects.create(products=product)
                return redirect('dashboard:best_product')
            except Product.DoesNotExist:
                return render(request, 'dashboard/add_best_product.html', {'error': 'Product does not exist.'})
    products = Product.objects.all()  # Get all products
    return render(request, 'dashboard/add_best_product.html', {'products': products})




def all_category(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'dashboard/All_Category.html', {'categories': categories})




def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('dashboard:all_category')



def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:  # Simple validation
            Category.objects.create(name=name)
            return redirect('dashboard:all_category')  # Assuming you have a view to list categories

    return render(request, 'dashboard/add_category.html')


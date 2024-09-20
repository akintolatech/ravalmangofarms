from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from django.contrib.auth.hashers import make_password ,check_password 
from dashboard.models import *
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth import authenticate, login


# Create your views here.

def index(request):



    category = Category.objects.get(name='Fresh Mango')
    AllCategory = Category.objects.all()


    Products  = Product.objects.filter(category=category.id)

    AllProducts = Product.objects.all()

    AllBestProducts = BestProducts.objects.all()



    context = {
        "ProductData":Products,
        "AllCategory":AllCategory,
        "AllProducts":AllProducts,
        "BestProducts":AllBestProducts
    }




    return render(request,'index.html',context)




def checkout(request):
    cart_items = CartItem.objects.all()
    subtotal = sum(item.total_price for item in cart_items)
    shipping = Decimal('3.00') 
    total = subtotal + shipping

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        town_city = request.POST.get('town_city')
        country = request.POST.get('country')
        postcode = request.POST.get('postcode')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        description = request.POST.get('description', '')
        
        uploaded_file = request.FILES.get('uploadedFile')

        # Create or get UserProfile instance
        user_profile, created = UserProfile.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'company_name': company_name,
                'address': address,
                'city': town_city,
                'country': country,
                'postcode': postcode,
                'mobile': mobile,
                'notes': description,
                'file': uploaded_file 
            }
        )

        # Loop through cart items and create FinalProduct instances
        for cart_item in cart_items:
            final_product = FinalProduct.objects.create(
                user_profile=user_profile,
                product_name=cart_item.product.name,
                price=cart_item.product.price,
                quantity=cart_item.quantity,
                total_price=cart_item.total_price,
                final_price=total,
                uploaded_file=cart_item.product.file  # Assuming product has a file field
            )

        # Clear the cart items after checkout
        cart_items.delete()

        return redirect('/')  # Redirect to home page after successful checkout

    return render(request, 'chackout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })




def cart_view(request):
    # user = Signup.objects.get(id=request.session['user_id'])  # Assuming you are using session-based authentication
    cart_items = CartItem.objects.all()
    subtotal = sum(item.total_price for item in cart_items)
    shipping = Decimal('3.00') 
    total = subtotal + shipping
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })




def add_to_cart(request, Product_id):
    # user = Signup.objects.get(id=request.session['user_id'])  # Assuming you are using session-based authentication
    product = get_object_or_404(Product, id=Product_id)
    
    cart_item, created = CartItem.objects.get_or_create(product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')  





def update_cart_item(request, cart_item_id, action):
    # user = Signup.objects.get(id=request.session['user_id'])
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return JsonResponse({'quantity': cart_item.quantity, 'total_price': cart_item.total_price})



def remove_from_cart(request, cart_item_id):
    # user = Signup.objects.get(id=request.session['user_id'])
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'status': 'success'})


# def signup(request):


#     context = {}

#     if request.method == 'POST':

#         first_name = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')



#         if Signup.objects.filter(email=email).exists():
#             context['error_message'] = 'User with this email already exists. Please use a different email.'
#             context['redirect_url'] = 'signup'


#         else:
             
#             hashed_password = make_password(password)

#             new_signup = Signup.objects.create(
#                name=first_name,
#                email=email,
#                password=hashed_password

#             )

#             context['success_message'] = 'Submitted successfully'
#             context['redirect_url'] = 'login'




#     return render(request,'signup.html',context)


# def login(request):

#     context = {}  
#     if request.method == 'POST':

#         email = request.POST.get('email')
#         password = request.POST.get('password')

        

#         try:
#             user = Signup.objects.get(email=email)

#             if check_password(password, user.password):
#                 request.session['user_id'] = user.id
#                 request.session['user_email'] = email
#                 request.session['user_name'] = user.name
#                 context['success_message'] = 'Login successful'


#             else:
#                 context['error_message'] = 'Invalid email or password. Please try again.'
#                 context['redirect_url'] = 'login'




#         except Signup.DoesNotExist:

#             context['error_message'] = 'Invalid email or password. Please try again.'
#             context['redirect_url'] = 'login'




#     return render(request,'login.html',context)


# def logout(request):
#     if 'user_email' in request.session:
#         del request.session['user_email']
#     if 'user_id' in request.session:
#         del request.session['user_id']
#     if 'user_name' in request.session:
#         del request.session['user_name']

#     message = {'success': 'Logged out successfully.'}
#     return render(request, 'index.html', {'message': message})




def Shop(request):  
    # Retrieve all categories
    AllCategory = Category.objects.all()

    # Retrieve featured products
    AllFeaturedProducts = FeaturedProduct.objects.all()
    paginator = Paginator(AllFeaturedProducts, 2)
    featurepage = request.GET.get('featurepage')
    page_obj = paginator.get_page(featurepage)

    # Retrieve the maximum price from the Product table
    max_price = Product.objects.aggregate(Max('price'))['price__max'] or 500  # Set a default max price if no products exist

    # Retrieve the price range from the request
    min_price = request.GET.get('min_price', 0)
    max_price_param = request.GET.get('max_price', max_price)

    # Filter products based on the price range
    AllProducts = Product.objects.filter(price__gte=min_price, price__lte=max_price_param)

    # Handle search query
    query = request.GET.get('search_query')
    if query:
        search_results = AllProducts.filter(name__icontains=query)
        

    else:
        search_results = []

    # Pagination for main product list
    total_products_per_page = 12  # You can adjust this number as needed
    paginator = Paginator(AllProducts, total_products_per_page)
    page_number = request.GET.get('page')
    try:
        paginatedProducts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginatedProducts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginatedProducts = paginator.page(paginator.num_pages)

    context = {
        'Categories': AllCategory,
        'paginatedProducts': paginatedProducts,
        'min_price': min_price,
        'max_price': max_price_param,
        'page_obj': page_obj,
        'search_results': search_results,
        'query': query,
    }

    return render(request, 'shop.html', context)




def ShopDetails(request,product_id):



    Product_Data = Product.objects.get(id=product_id)


    related_Products = Product.objects.filter(category=Product_Data.category.id)

    AllCategory  = Category.objects.all()


    AllFeaturedProducts = FeaturedProduct.objects.all()
    paginator = Paginator(AllFeaturedProducts, 2)
    featurepage = request.GET.get('featurepage')
    page_obj = paginator.get_page(featurepage)




    context = {
        'Product':Product_Data,
        'Categories':AllCategory,
        'page_obj': page_obj,
        'related_products':related_Products
    }

    return render(request,'shop-detail.html',context)




    return render(request,'shop-detail.html')





def Contact(request):
    
    return render(request,'contact.html')


def Adminlogin(request):

    if request.session.get('admin'):
        # If admin session already exists, redirect to admin dashboard

        return redirect('dashboard:dashboard')



    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            # Manually set user in the session

            request.session['admin'] = user.username

            success_message = "Login successful."
            
            # Redirect to admin dashboard or any other page
            return render(request, 'adminlogin.html', {'success_message': success_message})# Assuming 'admin_dashboard' is the name of the URL pattern for the admin dashboard
        else:
            # Authentication failed, show error messages
            error_message = "Invalid username or password."
            return render(request, 'adminlogin.html', {'error_message': error_message})


    else:
        return render(request, 'adminlogin.html')



def Adminlogout(request):
    # Check if the admin session exists
    if 'admin' in request.session:
        # Delete the admin session
        del request.session['admin']
    
    return redirect('/')  









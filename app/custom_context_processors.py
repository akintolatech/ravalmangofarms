
from dashboard.models import CartItem

from django.shortcuts import get_object_or_404

def session_value(request):
    return {
        'useremail': request.session.get('user_email'),
        'user_id': request.session.get('user_id'),
        'user_name': request.session.get('user_name'),
        'admin': request.session.get('admin')
        }



def cart_product_count(request):
    product_count = CartItem.objects.all().count()
    
    return {
        'product_count': product_count if product_count else 0
    }
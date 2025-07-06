from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.shortcuts import render
from .models import Profile, Cart, CartItem, Product, Order, OrderItem
from django.contrib.auth.models import User
from .models import Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from decimal import Decimal
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.http import Http404

# Create your views here.

@login_required
def shop(request):
    return render(request, 'shop/shop.html')

@never_cache
@login_required
def biscuits(request):
    products = Product.objects.filter(category='biscuit')
    return render(request, 'shop/biscuits.html', {'products': products})

@never_cache
@login_required
def snacks(request):
    products = Product.objects.filter(category='snack')
    return render(request, 'shop/snacks.html', {'products': products})

@never_cache
@login_required
def cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'shop/cart.html', {'cart': cart})

@never_cache
@login_required
def profile(request, username):
    profile = request.user.profile
    user = get_object_or_404(User, username=username)
    profile = user.profile
    if request.method == 'POST':
        if request.FILES.get('image'):
            profile.picture = request.FILES['image']

        profile.address = request.POST.get('address')
        
        profile.save()

        return redirect('profile',  username=username) 

    return render(request, 'shop/profile.html', {'profile': profile, 'user': request.user})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@never_cache
@login_required
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = request.session.get("cart", {})
        item_id = data["id"]

        if item_id in cart:
            cart[item_id]["quantity"] += 1
        else:
            cart[item_id] = {
                "name": data["name"],
                "price": data["price"],
                "quantity": 1,
                "weight": data["weight"],
                "image": data["image"]
            }

        request.session["cart"] = cart
        return JsonResponse({"cart": cart})
    print("📦 Received add_to_cart POST")


def remove_from_cart(request, product_id):
  cart = request.session.get('cart', {})
  if str(product_id) in cart:
      del cart[str(product_id)]
      request.session['cart'] = cart
  return JsonResponse({'status': 'removed', 'cart': cart})

@login_required
def get_cart(request):
    cart = request.session.get("cart", {})
    return JsonResponse({"cart": cart})

@csrf_exempt
@login_required
def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = request.session.get("cart", {})
        item_id = data.get("id")
        action = data.get("action")

        if item_id not in cart:
            return JsonResponse({"error": "Item not in cart"}, status=400)

        if action == "increment":
            cart[item_id]["quantity"] += 1
        elif action == "decrement":
            if cart[item_id]["quantity"] > 1:
                cart[item_id]["quantity"] -= 1
            else:
                del cart[item_id]
        elif action == "remove":
            del cart[item_id]
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)

        request.session["cart"] = cart
        return JsonResponse({"cart": cart})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return JsonResponse({'status': 'removed', 'cart': cart})


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):

    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        address = data.get('address')
        cart = request.session.get('cart', {})

        if not address or not cart:
            return JsonResponse({'message': 'Address and cart are required'}, status=400)

        order = Order.objects.create(user=request.user, address=address)

        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=Decimal(item['price'])
            )

        # clear cart
        request.session['cart'] = {}
        request.session.modified = True

        return JsonResponse({'message': 'Order placed successfully', 'redirect_url': '/cart/?reload=true'})

    
@login_required
def admin_orders(request):
    if not request.user.is_superuser:
        return redirect('shop')

    orders = Order.objects.all().order_by('-ordered_at')
    return render(request, 'shop/admin_orders.html', {'orders': orders})

@login_required
def user_orders(request, username):
    # Only allow viewing own orders or superuser
    if request.user.username != username and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to view this page.")

    orders = Order.objects.filter(user__username=username).order_by('-ordered_at')
    return render(request, 'shop/user_orders.html', {'orders': orders, 'username': username})

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@csrf_exempt
@login_required
@require_POST
def take_order(request, order_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        order = Order.objects.get(id=order_id)
        order.is_taken = True
        order.status_message = f"Your order #{order.id} has been taken and is being processed by admin!"
        order.save()

        return JsonResponse({'message': f'Order #{order.id} has been taken.'})

    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


@login_required
def chat_room(request):
    messages = Message.objects.all()
    context = {
        'messages': messages,
        'user': request.user  # <- add this
    }
    return render(request, 'shop/chat.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(sender=request.user, content=content)
    return redirect('chat_room')

def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        if message.sender == request.user:
            message.delete()
    except Message.DoesNotExist:
        raise Http404("Message not found.")
    return redirect('chat_room')

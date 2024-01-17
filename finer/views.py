from django.shortcuts import render, redirect,get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from .models import User,Product,ShippingAddress,Cart,OrderItem,Order,Feedback
from django.db.models import Q,Count,Sum
from django.http import HttpResponse,JsonResponse
from decimal import Decimal
import random
from django.utils import timezone


def home(request):
    random_products = Product.objects.all().order_by('?')[:3]
    return render(request, 'index.html', {'random_products': random_products})


def user(request):
    return render(request, 'user_register.html')

def login(request):
    return render(request, 'pages-login.html')

def admin(request):
    return render(request, 'admin_login.html')

def product(request):
    return render(request, 'addproduct.html')

def users(request):
    return render(request, 'users.html')

def user_feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback', '')

        if feedback_text:
            user_id = request.session.get('uid')  
            user_feedback = Feedback.objects.create(text=feedback_text, user_id=user_id)
            messages.success(request, "Feedback submitted successfully!")

        else:
            messages.error(request, "Feedback cannot be empty.")

def feedback_details(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback.html', {'feedbacks': feedbacks})

    return redirect('user_home')
def user_home(request):
    random_products = Product.objects.all().order_by('?')[:3]
    return render(request, 'user_home.html', {'random_products': random_products})

def saree(request):
    saree = Product.objects.filter(subtype='Saree')
    return render(request, 'saree.html', {'saree': saree})

def churidar(request):
    churidar = Product.objects.filter(subtype='Churidar')
    return render(request, 'churidar.html', {'churidar': churidar})

def shirt(request):
    shirts = Product.objects.filter(subtype='Shirt')
    return render(request, 'shirt.html', {'shirts': shirts})

def tshirt(request):
    tshirts = Product.objects.filter(subtype='T-Shirt')
    print("Number of T-shirts:", len(tshirts))  # Add this line
    return render(request, 'tshirt.html', {'tshirts': tshirts})

def checkout_view(request, product_price):
    return render(request, 'checkout.html', {'product_price': product_price})
    
def checkout(request, total_amount=None):
    if total_amount is None:
        total_amount = request.GET.get('total_amount', '0.00')

    user_id = request.session.get('uid')
    user = User.objects.get(id=user_id) if user_id else None

    previous_shipping_address = None
    if user:
        previous_shipping_address = ShippingAddress.objects.filter(user=user).order_by('-order_date').first()

    if request.method == 'POST':
       
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')

       
        shipping_address = ShippingAddress.objects.create(
            user=user,
            fullname=fullname,
            phone=phone,
            email=email,
            pincode=pincode,
            address=address
        )
        order_number = random.randint(100000, 999999)
  
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            amount=float(total_amount),
            order_date=timezone.now(),
            order_number=order_number
        )

     
        cart_items = Cart.objects.filter(uid=user)
        for cart_item in cart_items:
            product = cart_item.pid
            quantity = cart_item.quantity
            total_price = cart_item.total_price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                total_price=total_price
            )

  
        Cart.objects.filter(uid=user).delete()

        return redirect('order_confirm', order_date=str(order.order_date))

    return render(request, 'checkout.html', {'total_amount': total_amount, 'previous_shipping_address': previous_shipping_address})

def order_confirm(request, order_date=None):
    # Fetch the order details based on the order_date (replace this with your actual retrieval code)
    # Note: You might need to convert order_date to the appropriate datetime format used in your model
    order = Order.objects.get(order_date=order_date)

    # Fetch the username from the session
    uname = request.session.get('uname', '')

    # Include the order details, total amount, and username in the context
    context = {
        'order': order,
        'order_number': order.order_number,  # Assuming the order number is stored in the 'order_number' field
        'uname': uname,
        'total_amount': order.amount,  # Assuming the total amount is stored in the 'amount' field
        'order_date': order.order_date,
        # Add other context variables as needed
    }

    return render(request, 'order_confirm.html', context)

def calculate_total(cart_items):
    # Calculate the total amount based on quantity and price of each item in the cart
    total = sum(item.quantity * item.total_price for item in cart_items)
    return total

def payment_gateway(request):
    return render(request, 'payment_gateway.html')


def shirt_collection(request):
    shirts = Product.objects.filter(subtype='Shirt')
    return render(request, 'shirt.html', {'shirts': shirts})

def cart(request):
    userid = request.session.get('uid')

    cart_items = Cart.objects.filter(uid = userid)
    item_details = Cart.objects.filter(uid = userid)
    
    total_amount = 0
    for i in item_details:
        total_amount += i.total_price

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount':total_amount})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_price = float(product.price)
    user_id = request.session.get('uid')
    user = User.objects.get(id=user_id)
    cart_obj = Cart.objects.filter(uid=user, pid=product)

    if cart_obj.exists():
        updation_data = Cart.objects.get(uid=user, pid=product)
        updation_data.quantity += 1
        updation_data.save()

        updation_data.total_price = updation_data.quantity * product_price
        updation_data.save()
    else:
        Cart.objects.create(
            uid=user,
            pid=product,
            quantity=1,
            total_price=1 * product_price
        )

    messages.success(request, f"{product.name} added to cart!")

    return redirect(request.META['HTTP_REFERER'])

    

def remove_from_cart(request, item_id):
    userid = request.session.get('uid')

    # Assuming 'uid' is the field in your Cart model representing the user identifier
    cart_item = Cart.objects.filter(uid=userid, pid__id=item_id).first()

    if cart_item:
        cart_item.delete()

    return redirect('cart')

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('quantity'))

        # Assuming 'uid' is the field in your Cart model representing the user identifier
        user_id = request.session.get('uid')

        cart_item = Cart.objects.filter(uid=user_id, pid__id=product_id).first()

        if cart_item:
            cart_item.quantity = new_quantity
            cart_item.total_price = new_quantity * cart_item.pid.price
            cart_item.save()

            total_amount = Cart.objects.filter(uid=user_id).aggregate(Sum('total_price'))['total_price__sum']

            return JsonResponse({'success': True, 'total_amount': total_amount})

    return JsonResponse({'success': False})

def admin_home(request):
    total_product_count = Product.objects.aggregate(total_products=Count('id'))
    total_user_count = User.objects.count()
    total_orders_count = Order.objects.count()
    return render(request, 'admin_home.html', {'total_product_count': total_product_count, 'total_user_count': total_user_count,'total_orders_count' :total_orders_count})

def view_orders(request):
    orders = Order.objects.all()
    return render(request, 'view_orders.html', {'orders': orders})


def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        product_description = request.POST.get('productDescription')
        product_category = request.POST.get('productCategory')
        product_subtype = request.POST.get('productSubtype')
        product_image = request.FILES.get('productImage') 
        product_price = request.POST.get('productPrice')


        new_product = Product(
            name=product_name,
            description=product_description,
            category=product_category,
            subtype=product_subtype,
            image=product_image,
            price=product_price
        )

        new_product.save()

        messages.success(request, 'Product added successfully!')
        return redirect('add_product')

    return render(request, 'addproduct.html')

def get_subtypes(request):
    category = request.GET.get('category')
    subtypes = []

    if category == 'Women':
        subtypes = ['Saree', 'Churidar']
    elif category == 'Men':
        subtypes = ['T-Shirt', 'Shirt']

    return JsonResponse({'subtypes': subtypes})

def view_products(request):
    search_query = request.GET.get('search', '')

    products = Product.objects.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(category__icontains=search_query)
    )

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                product.delete()
                messages.success(request, 'Product deleted successfully!')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')

            return redirect('view_products')

    return render(request, 'view_products.html', {'products': products})

def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
    
    return redirect('view_products')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin':
            return redirect('admin_home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_login.html')


def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken. Please choose a different one.')
                return render(request, 'user_register.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered. Please use a different one.')
                return render(request, 'user_register.html')

            user = User(name=name, email=email, username=username, password=password)
            user.save()

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login_user')

        except IntegrityError as e:
            messages.error(request, 'Error creating user.')
            return render(request, 'user_register.html')

    return render(request, 'user_register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username,password=password).exists():
            data=User.objects.filter(username=username,password=password).values().first()
            request.session['uname']=data['name']
            request.session['uemail']=data['email']
            request.session['usname']=data['username']
            request.session['upass']=data['password']
            request.session['uid']=data['id']
            return redirect('user_home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'pages-login.html')


def registered_users(request):
    search_query = request.GET.get('search', '')
    
    users = User.objects.filter(
        Q(name__icontains=search_query) |
        Q(username__icontains=search_query) |
        Q(email__icontains=search_query)
    )
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                messages.success(request, 'User deleted successfully!')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')

            return redirect('registered_users')

    return render(request, 'registered-users.html', {'users': users})

def logout(request):
    del request.session['uname']
    del request.session['uemail']
    del request.session['usname']
    del request.session['upass']
    del request.session['uid']
    return redirect('index')
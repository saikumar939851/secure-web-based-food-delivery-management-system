from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Sum
from django.contrib import messages


# ---------------- HOME ----------------

def home(request):
    return render(request, 'home.html')


# ---------------- AUTH ----------------

def user_register(request):
    if request.method == 'POST':
        User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            role='user'
        )
        messages.success(request, "Registered Successfully")
        return redirect('user_login')
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'restaurant':
                return redirect('restaurant_dashboard')
            else:
                return redirect('browse_restaurants')

        except:
            messages.error(request, "Invalid Login")

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


# ---------------- ADMIN ----------------

def admin_dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('user_login')

    restaurants = User.objects.filter(role='restaurant')
    return render(request, 'admin/dashboard.html', {'restaurants': restaurants})

def restaurant_dashboard(request):

    if request.session.get('role') != 'restaurant':
        return redirect('login')

    user_id = request.session.get('user_id')
    request.session['restaurant_name'] = restaurant.name
    request.session['restaurant_email'] = restaurant.email
    

    restaurant = User.objects.get(id=user_id)
    foods = FoodItem.objects.filter(restaurant_id=user_id)
    total_foods = foods.count()

    return render(request, 'restaurant/dashboard.html', {
        'restaurant': restaurant,
        'foods': foods,
        'total_foods': total_foods
    })

def add_restaurant(request):
    if request.method == 'POST':
        User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            role='restaurant'
        )
        return redirect('admin_dashboard')

    return render(request, 'admin/add_restaurant.html')


def delete_restaurant(request, id):
    User.objects.filter(id=id).delete()
    return redirect('admin_dashboard')


def view_orders_admin(request):
    orders = Order.objects.all()
    return render(request, 'admin/view_orders.html', {'orders': orders})


# ---------------- RESTAURANT ----------------

def restaurant_register(request):
    if request.method == 'POST':
        User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            role='restaurant'
        )
        return redirect('user_login')

    return render(request, 'restaurant/register.html')


def restaurant_dashboard(request):
    foods = FoodItem.objects.filter(restaurant_id=request.session['user_id'])
    return render(request, 'restaurant/dashboard.html', {'foods': foods})


def add_category(request):
    if request.method == 'POST':
        Category.objects.create(
            name=request.POST['name'],
            restaurant_id=request.session['user_id']
        )
        return redirect('restaurant_dashboard')
    return render(request, 'restaurant/add_category.html')


def add_food(request):

    if request.method == 'POST':
        FoodItem.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            image=request.FILES['image'],   # important
            category_id=request.POST['category'],
            restaurant_id=request.session['user_id']
        )

        return redirect('restaurant_dashboard')

    categories = Category.objects.filter(restaurant_id=request.session['user_id'])

    return render(request,'restaurant/add_food.html',{'categories':categories})



def delete_food(request, id):
    FoodItem.objects.filter(id=id).delete()
    return redirect('restaurant_dashboard')


def view_orders_restaurant(request):
    orders = Order.objects.filter(restaurant_id=request.session['user_id'])
    return render(request, 'restaurant/view_orders.html', {'orders': orders})


def update_order_status(request, id):
    order = Order.objects.get(id=id)
    order.status = request.POST['status']
    order.save()
    return redirect('view_orders_restaurant')


# ---------------- USER ----------------

def browse_restaurants(request):
    restaurants = User.objects.filter(role='restaurant')
    return render(request, 'user/browse.html', {'restaurants': restaurants})


def view_menu(request, id):
    foods = FoodItem.objects.filter(restaurant_id=id)
    return render(request, 'user/menu.html', {'foods': foods})


def add_to_cart(request, id):
    Cart.objects.create(
        user_id=request.session['user_id'],
        food_id=id,
        quantity=1
    )
    return redirect('view_cart')


def view_cart(request):
    cart = Cart.objects.filter(user_id=request.session['user_id'])
    total = cart.aggregate(total=Sum('food__price'))['total']
    return render(request, 'user/cart.html', {'cart': cart, 'total': total})


def remove_from_cart(request, id):
    Cart.objects.filter(id=id).delete()
    return redirect('view_cart')


def place_order(request):
    cart_items = Cart.objects.filter(user_id=request.session['user_id'])

    total = sum(item.food.price for item in cart_items)

    order = Order.objects.create(
        user_id=request.session['user_id'],
        restaurant_id=cart_items.first().food.restaurant_id,
        total_amount=total,
        status='Pending'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order_id=order.id,
            food_id=item.food.id,
            quantity=item.quantity,
            price=item.food.price
        )

    cart_items.delete()
    return redirect('my_orders')


def my_orders(request):
    orders = Order.objects.filter(user_id=request.session['user_id'])
    return render(request, 'user/my_orders.html', {'orders': orders})
def add_category(request):

    if request.session.get('role') != 'restaurant':
        return redirect('login')

    user_id = request.session.get('user_id')

    if request.method == 'POST':
        Category.objects.create(
            name=request.POST['name'],
            restaurant_id=user_id
        )
        return redirect('add_category')

    categories = Category.objects.filter(restaurant_id=user_id)

    return render(request, 'restaurant/add_category.html', {
        'categories': categories
    })
def delete_category(request, id):

    if request.session.get('role') != 'restaurant':
        return redirect('login')

    user_id = request.session.get('user_id')

    category = get_object_or_404(Category, id=id, restaurant_id=user_id)
    category.delete()

    return redirect('add_category')
def cancel_order(request, id):

    if request.session.get('role') != 'user':
        return redirect('login')

    user_id = request.session.get('user_id')

    order = get_object_or_404(Order, id=id, user_id=user_id)

    # Allow cancel only if still pending
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()

    return redirect('my_orders')
def admin_dashboard(request):

    if request.session.get('role') != 'admin':
        return redirect('login')

    restaurants = User.objects.filter(role='restaurant')
    users = User.objects.filter(role='user')
    categories = Category.objects.all()
    foods = FoodItem.objects.all()
    orders = Order.objects.all()

    return render(request, 'admin/dashboard.html', {
        'restaurants': restaurants,
        'users': users,
        'categories': categories,
        'foods': foods,
        'orders': orders
    })
def admin_dashboard(request):

    if request.session.get('role') != 'admin':
        return redirect('login')

    restaurants = User.objects.filter(role='restaurant')
    users = User.objects.filter(role='user')
    foods = FoodItem.objects.all()
    orders = Order.objects.all()
    feedbacks = Feedback.objects.all()
    feedback_count = feedbacks.count()

    return render(request, 'admin/dashboard.html', {
        'restaurants': restaurants,
        'users': users,
        'foods': foods,
        'orders': orders,
        'feedbacks': feedbacks,
        'feedback_count': feedback_count
    })

def delete_food_admin(request, id):

    if request.session.get('role') != 'admin':
        return redirect('login')

    FoodItem.objects.filter(id=id).delete()
    return redirect('admin_dashboard')
def delete_user(request, id):

    if request.session.get('role') != 'admin':
        return redirect('login')

    User.objects.filter(id=id, role='user').delete()
    return redirect('admin_dashboard')
def add_feedback(request, restaurant_id):

    if request.session.get('role') != 'user':
        return redirect('login')

    user_id = request.session.get('user_id')

    restaurant = get_object_or_404(User, id=restaurant_id, role='restaurant')

    if request.method == 'POST':
        Feedback.objects.create(
            user_id=user_id,
            restaurant=restaurant,
            message=request.POST['message'],
            rating=request.POST['rating']
        )
        return redirect('browse_restaurants')

    return render(request, 'user/add_feedback.html', {
        'restaurant': restaurant
    })
def add_feedback(request, restaurant_id):

    if request.session.get('role') != 'user':
        return redirect('login')

    user_id = request.session.get('user_id')

    restaurant = get_object_or_404(User, id=restaurant_id, role='restaurant')

    if request.method == 'POST':
        Feedback.objects.create(
            user_id=user_id,
            restaurant=restaurant,
            message=request.POST['message'],
            rating=request.POST['rating']
        )
        return redirect('browse_restaurants')

    return render(request, 'user/add_feedback.html', {
        'restaurant': restaurant
    })
def view_feedback_admin(request):

    if request.session.get('role') != 'admin':
        return redirect('login')

    feedbacks = Feedback.objects.all()

    return render(request, 'admin/view_feedback.html', {
        'feedbacks': feedbacks
    })
def view_feedback_restaurant(request):

    if request.session.get('role') != 'restaurant':
        return redirect('login')

    restaurant_id = request.session.get('user_id')

    feedbacks = Feedback.objects.filter(restaurant_id=restaurant_id)

    return render(request, 'restaurant/view_feedback.html', {
        'feedbacks': feedbacks
    })

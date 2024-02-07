from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import logging
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.

#


def create_shipping_address(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    phone_number = request.POST.get('phone_number')
    city = request.POST.get('city')
    additional_information = request.POST.get('additional_information')

    ShippingAddress.objects.create(
        user=request.user,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        city=city,
        additional_information=additional_information
    )

    return redirect('core:payment_type')


def shipping_address(request):
    return render(request, 'checkout/shipping address.html')


def payment_type(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_amount = cart_items.aggregate(total=Sum('subtotal'))['total'] or 0

    delivery_fees = {'Dei_dei': 500, 'Kado': 1500,
                     'Within_Abuja': 2000, 'in_store': 0}

    # Default to 'AL' if not provided
    selected_city = request.GET.get('city', 'AL')
    delivery_fee = delivery_fees.get(selected_city, 0)

    context = {
        'total_amount': total_amount,
        'delivery_fees': delivery_fees,
        'selected_city': selected_city,
        'delivery_fee': delivery_fee,
        'user': request.user
    }

    return render(request, 'checkout/payment_type.html', context)


def create_order(request, totalPrice, payment_type):
    try:
        user_cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)

        with transaction.atomic():
            shipping_address = ShippingAddress.objects.filter(
                user=request.user).first()
            new_order = Order.objects.create(
                user=request.user,
                address=shipping_address,
                total_price=totalPrice,
                payment_type=payment_type,
                status='pending'
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=new_order,
                    meal=cart_item.meal,
                    quantity=cart_item.quantity,
                    subtotal=cart_item.subtotal
                )

            cart_items.delete()
            order_items = OrderItem.objects.filter(order=new_order)
            merge_data = {
                'order': new_order,
                'shipping_address': shipping_address,
                'order_items': order_items,
            }

            html_body = render_to_string(
                "emails/product_alert.html", merge_data)
            msg = EmailMultiAlternatives(
                subject=f"Website Order Placed Mail",
                from_email=settings.EMAIL_HOST_USER,
                to=["goldianikenterprise@yahoo.com"],
                body=" ",
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)

        return redirect('core:success')

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")

        # Redirect the user to an error page or handle the error as needed
        return redirect('core:failure')


def index(request):
    meals = Meal.objects.all()[:8]
    testimonials = Testimonial.objects.all()

    context = {
        'meals': meals,
        'testimonials': testimonials,
    }

    return render(request, 'index.html', context)


def menu_detail(request, pk):
    meal = get_object_or_404(
        Meal, pk=pk)

    context = {
        'meal': meal,
    }

    return render(request, 'menu/menu_details.html', context)


def about(request):
    return render(request, 'about/about.html')


def menu(request, tag=None):

    meals = Meal.objects.all().order_by('name')
    tags = Tag.objects.all()

    query = request.GET.get('query')

    print(f"the query is {query}")

    if tag:
        meals = meals.filter(tag__name=tag)

    if query:
        meals = Meal.objects.filter(name__icontains=query)

    meals_per_page = 10
    paginator = Paginator(meals, meals_per_page)
    page = request.GET.get('page')
    print(meals)
    try:
        current_meal = paginator.page(page)
    except PageNotAnInteger:
        current_meal = paginator.page(1)
    except EmptyPage:
        current_meal = paginator.page(paginator.num_pages)

    context = {
        'meals': current_meal,
        'tags': tags,
    }

    return render(request, 'menu/menu.html', context)


def contact(request):
    return render(request, 'contact/contact.html')


def checkout(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_amount = cart_items.aggregate(total=Sum('subtotal'))['total'] or 0

    delivery_fees = {'Dei_dei': 500, 'Kado': 1500, 'Within_Abuja': 2000}

    # Default to 'AL' if not provided
    selected_city = request.GET.get('city', 'AL')
    delivery_fee = delivery_fees.get(selected_city, 0)

    context = {
        'total_amount': total_amount,
        'cart_length': len(cart_items),
        'delivery_fees': delivery_fees,
        'selected_city': selected_city,
        'delivery_fee': delivery_fee,
        'user': request.user
    }

    return render(request, 'checkout/checkout.html', context)


@login_required(login_url='authorization:login')
def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_amount = cart_items.aggregate(total=Sum('subtotal'))['total'] or 0

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_length': len(cart_items),
    }

    return render(request, 'cart/cart_main.html', context)


@login_required(login_url='authorization:login')
def cartAdd(request, meal_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity is not None and quantity != 0 and quantity != "":
            print("quantity ID:", request.POST.get('quantity'))
            quantity = int(request.POST.get('quantity'))
        else:
            quantity = int(1)
        print("Meal ID:", meal_id)
        meal = Meal.objects.get(id=meal_id)
        subtotal = calculate_subtotal(meal, quantity)

        user_cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=user_cart,
            meal=meal,
            defaults={
                'quantity': quantity,
                'subtotal': subtotal,
            }
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.subtotal = calculate_subtotal(meal, cart_item.quantity)
            cart_item.save()

        return redirect('core:cart')

    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)
        total_amount = cart_items.aggregate(
            total=Sum('subtotal'))['total'] or 0

        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
            'cart_length': len(cart_items),
        }

        return render(request, 'cart/cart_main.html', context)
    else:
        return redirect('authorization:login')


def calculate_subtotal(meal, quantity):
    return meal.price * quantity


def success(request):
    return render(request, 'alert/success.html')


def failure(request):
    return render(request, 'alert/failure.html')


def cartRemove(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.cart.user == request.user:
        cart_item.delete()
    return redirect('core:cart')


@csrf_exempt  # Use this decorator to exempt CSRF validation for demonstration purposes
def send_purchase_receipt_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        subscribe = request.POST.get('subscribe')

        # Your existing email sending logic goes here...
        try:
            merge_data = {
                'name': name,
                'phone_number': phone,
                'message': message,
            }

            html_body = render_to_string(
                "emails/confirmation.html", merge_data)
            msg = EmailMultiAlternatives(
                subject=f"Website Contact Mail: {subject}",
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
                body=" ",
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)

            return render(request, 'contact/contact.html')
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"An error occurred: {e}", exc_info=True)
            return render(request, {"error": "An internal server error occurred."}, status=500)

    return render(request, 'contact/contact.html')

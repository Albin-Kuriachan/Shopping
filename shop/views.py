import re

from django.contrib import messages
from django.db import transaction
from django.db.models import F, Min
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from account.models import CustomUser
from .models import Cart, Address, Payment, Review
from product.models import ProductDetails, Quantity, Category
from .forms import AddressForm
from .send_email import send_email




def index(request):
    product_data = ProductDetails.objects.all()
    category_data = Category.objects.all()
    cart_items_count = cart_count(request)

    if request.method == 'POST':
        products = request.POST.get('products')

        if products:
            product_data = product_data.filter(product_name__iregex=products)

    context = {
        'product_data': product_data,
        'category_data': category_data,
        'cart_items_count': cart_items_count
    }

    return render(request, 'index.html', context)


# def category(request,id):
#     product_data = ProductDetails.objects.filter(category_id=id)
#
#     context = {
#
#         'product_data': product_data,
#     }
#     return render(request, 'category.html')


def category(request, id):
    category_instance = Category.objects.get(pk=id)
    product_data = ProductDetails.objects.filter(category=category_instance)

    context = {
        'product_data': product_data,
    }
    return render(request, 'category.html', context)


def single_product(request, pk, pid):
    user = request.user
    single_data = get_object_or_404(ProductDetails, id=pk)
    price_data = single_data.quantity_set.filter(id=pid).first()
    weight = single_data.quantity_set.all()
    reviews = Review.objects.filter(cart__product=pk).order_by('-id')
    write_review = Review.objects.filter(cart__product=pk, cart__stage='Order').first()
    # ord = Cart.objects.filter(user_id=user.id, cart__stage='Order').first()
    related_product = ProductDetails.objects.filter(category__in=single_data.category.all())
    cart_item_exists = Cart.objects.filter(user__id=user.id, product_id=pk, quantity_id=pid, stage='Cart').exists()
    cart_item_review = Cart.objects.filter(user__id=user.id, product_id=pk, quantity_id=pid, stage='Order').exists()


    if request.method == 'POST':
        my_review = request.POST.get('review')

        data = Review(my_review=my_review, user=user, cart=write_review.cart)
        data.save()
    cart_items_count = cart_count(request)
    context = {
        'single_data': single_data,
        'price_data': price_data,
        'weight': weight,
        'related_product': related_product,
        'cart_item_exists': cart_item_exists,
        'reviews': reviews,
        'write_review': write_review,
        'cart_items_count': cart_items_count,
        'cart_item_review': cart_item_review,
    }
    return render(request, 'single-product.html', context)


# def save_review(request):
#     return  redirect(single_product)

def cart(request):
    user = request.user
    cart_data = Cart.objects.filter(user_id=user.id, stage='Cart')
    cart_items_count = cart_count(request)
    context = {
        'cart_data': cart_data,
        'cart_items_count': cart_items_count
    }
    return render(request, 'cart.html', context)


def add_cart(request, product_id, quantity_id):
    user = request.user
    # userdata=CustomUser.objects.get(email=user)
    product = get_object_or_404(ProductDetails, id=product_id)
    quantity = get_object_or_404(Quantity, product_id=product.id, id=quantity_id)

    cart_item_exists = Cart.objects.filter(user_id=user.id, product=product_id, quantity_id=quantity_id,
                                           stage='Cart').exists()
    if cart_item_exists:
        no = Cart.objects.get(user_id=user.id, product=product_id, quantity_id=quantity_id, stage='Cart')

        if quantity.no_quantity > no.selected_no:
            no.selected_no += 1
            no.total = no.selected_no * no.unit_price
            no.save()
    else:
        Cart.objects.create(user_id=user.id, product_id=product.id, quantity_id=quantity.id, unit_price=quantity.price,
                            selected_no=1, total=quantity.price, product_name=product.product_name,
                            product_quantity=str(quantity.weight_litter) + quantity.denominations)
    return redirect('cart')


def substrate_cart(request, product_id, quantity_id):
    user = request.user
    no = Cart.objects.get(user_id=user.id, product=product_id, quantity_id=quantity_id, stage='Cart')

    if no.selected_no > 1:
        no.selected_no -= 1
        no.total = no.selected_no * no.unit_price
        no.save()
    return redirect('cart')


def remove_from_cart(request, product_id, quantity_id):
    user = request.user
    try:
        cart_item = Cart.objects.get(user_id=user.id, product_id=product_id, quantity_id=quantity_id,stage='Cart')
    except Cart.DoesNotExist:
        pass
    else:
        cart_item.delete()

    return redirect(cart)


def wishlist(request):
    cart_items_count = cart_count(request)
    context = {

        'cart_items_count': cart_items_count
    }
    return render(request, 'wishlist.html',context)


def select_address(request):
    user = request.user
    address_data = Address.objects.filter(user_id=user.id)
    # if request.method == 'POST':
    #     form = AddressForm(request.POST)
    #     if form.is_valid():
    #         data = form.save(commit=False)
    #         data.user = user
    #         data.save()

    form = AddressForm()
    context = {
        'address_data': address_data, 'form': form
    }
    return render(request, 'select_address.html', context)


def add_address(request):
    user = request.user
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
        return redirect(select_address)

    # else:
    #     return redirect(select_address)
    #     form = AddressForm()
    # return render(request, 'address_form.html', {'form': form})


def set_as_default(request, address_id):
    user = request.user
    address = Address.objects.get(user_id=user.id, id=address_id)
    address.is_default = True
    address.save()
    return redirect(select_address)


def edit_address(request, address_id):
    user = request.user
    address = get_object_or_404(Address, id=address_id)

    if address.user != user:
        return redirect('select_address')

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return redirect('select_address')
    else:
        form = AddressForm(instance=address)

    return render(request, 'address_form.html', {'form': form})


def delete_address(request, address_id):
    Address.objects.filter(id=address_id).delete()
    return redirect('select_address')


def order_preview(request):
    user = request.user
    cart_data = Cart.objects.filter(user_id=user.id, stage='Cart')
    address_id = request.GET.get('address_id')

    if address_id is not None:
        address_choosed = Address.objects.get(id=address_id)
    else:
        return redirect('address_list')

    grand_total = sum(cart.total for cart in cart_data)

    context = {
        'address_choosed': address_choosed,
        'cart_data': cart_data,
        'grand_total': grand_total,
    }
    return render(request, 'order_preview.html', context)


def place_order(request, address_id):
    user = request.user
    address_data = get_object_or_404(Address, id=address_id)
    cart_items = Cart.objects.filter(user_id=user.id)
    for cart_item in cart_items:
        # cart_item.address = f"{address_data.first_name} {address_data.last_name}, {address_data.address_line}"
        full_address = f"{address_data.first_name} {address_data.last_name}, {address_data.address_line}," \
                       f" {address_data.pin_code}, {address_data.place},{address_data.phone},{address_data.phone2}, {address_data.landmark}"

        cart_item.address = full_address

        cart_item.stage = 'Order'
        cart_item.save()
    product_count_remove(request)

    email = user.email
    subject = 'Order Placed'
    message = f' Yor Order Placed successfully'
    send_email(email, subject, message)
    messages.success(request, 'Order placed successfully')
    return redirect('order_view')


def product_count_remove(request):
    user = request.user
    cart_items = Cart.objects.filter(user_id=user.id)
    for cart_item in cart_items:
        no_item = cart_item.selected_no
        product = Quantity.objects.get(id=cart_item.quantity.id)
        product_count = product.no_quantity
        product_new_count = product_count - no_item
        with transaction.atomic():
            product.no_quantity = product_new_count
            product.save()


def payment(request, id):
    user = request.user
    card_data = Payment.objects.filter(user=user)
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        month = request.POST.get('month')
        year = request.POST.get('year')
        data = Payment(card_number=card_number, month=month, year=year, user=user)
        data.save()
        return redirect('payment')
    else:

        return render(request, 'payment.html', {'card_data': card_data, 'id': id})


def delete_payment(request, id):
    Payment.objects.get(id=id).delete()
    return redirect('payment')


def order_view(request):
    user = request.user
    order_data = Cart.objects.filter(user_id=user.id, stage='Order').order_by('-id')
    cart_items_count = cart_count(request)
    context = {
        'order_data': order_data,
        'cart_items_count': cart_items_count
    }
    return render(request, 'order_view.html', context)


def base(request):
    product_data = ProductDetails.objects.all()
    category_data = Category.objects.all()

    if request.method == 'POST':
        products = request.POST.get('products')

        if products:
            product_data = product_data.filter(product_name__iregex=products)

    context = {
        'product_data': product_data,
        'category_data': category_data
    }

    return render(request, 'base.html', context)


#
# from django.db.models import F
#
# def filter(request):
#     product_data = ProductDetails.objects.all()
#     if request.method == 'POST':
#         from_price = request.POST.get('from_price')
#         to_price = request.POST.get('to_price')
#
#         if from_price is None:
#             from_price = 1
#
#         if to_price is None:
#             to_price = 1000
#
#         if from_price is not None and to_price is not None:
#             product_data = product_data.filter(quantity__price__range=(from_price, to_price))
#     context = {
#         'product_data': product_data
#     }
#
#     return render(request, "filter.html", context)


def filter(request):
    product_data = ProductDetails.objects.all()

    if request.method == 'POST':
        from_price = request.POST.get('from_price')
        to_price = request.POST.get('to_price')

        if not from_price:
            from_price = 1
        if not to_price:
            to_price = 1000

        product_data = product_data.filter(quantity__price__range=(from_price, to_price))

    context = {
        'product_data': product_data
    }

    return render(request, "filter.html", context)


def low_to_high(request):
    product_data = ProductDetails.objects.annotate(
        min_price=Min('quantity__price')
    ).order_by('min_price')

    context = {
        'product_data': product_data
    }
    return render(request, "filter.html", context)


def high_to_low(request):
    product_data = ProductDetails.objects.annotate(
        max_price=Min('quantity__price')
    ).order_by('-max_price')

    context = {
        'product_data': product_data
    }
    return render(request, "filter.html", context)


def cart_count(request):
    user = request.user
    order_data = Cart.objects.filter(user_id=user.id, stage='Cart')
    order_count = order_data.count
    return order_count

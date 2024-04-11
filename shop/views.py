from django.db.models import F
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Cart, Address, Order
from product.models import ProductDetails, Quantity, Category
from .forms import AddressForm


# Create your views here.


def index(request):
    product_data = ProductDetails.objects.all()
    category_data = Category.objects.all()

    context = {
        'product_data': product_data,
        'category_data': category_data
    }

    return render(request, 'index.html', context)


def single_product(request, pk, pid):
    user = request.user
    single_data = get_object_or_404(ProductDetails, id=pk)
    price_data = single_data.quantity_set.filter(id=pid).first()
    weight = single_data.quantity_set.all()
    related_product = ProductDetails.objects.filter(category__in=single_data.category.all())
    cart_item_exists = Cart.objects.filter(user__id=user.id, product_id=pk, quantity_id=pid).exists()
    print(cart_item_exists)

    context = {
        'single_data': single_data,
        'price_data': price_data,
        'weight': weight,
        'related_product': related_product,
        'cart_item_exists': cart_item_exists,
    }
    return render(request, 'single-product.html', context)


def cart(request):
    user = request.user
    cart_data = Cart.objects.filter(user_id=user.id)
    context = {
        'cart_data': cart_data,
    }
    return render(request, 'cart.html', context)


def add_cart(request, product_id, quantity_id):
    user = request.user
    product = get_object_or_404(ProductDetails, id=product_id)
    quantity = get_object_or_404(Quantity, product_id=product.id, id=quantity_id)

    cart_item_exists = Cart.objects.filter(user_id=user.id, product=product_id, quantity_id=quantity_id).exists()
    if cart_item_exists:
        no = Cart.objects.get(user_id=user.id, product=product_id, quantity_id=quantity_id)

        if quantity.no_quantity > no.selected_no:
            no.selected_no += 1
            no.total = no.selected_no * no.unit_price
            no.save()
    else:
        Cart.objects.create(user_id=user.id, product_id=product.id, quantity_id=quantity.id, unit_price=quantity.price,
                            selected_no=1, total=quantity.price)
    return redirect('cart')


def substrate_cart(request, product_id, quantity_id):
    user = request.user
    no = Cart.objects.get(user_id=user.id, product=product_id, quantity_id=quantity_id)

    if no.selected_no > 1:
        no.selected_no -= 1
        no.total = no.selected_no * no.unit_price
        no.save()
    return redirect('cart')


def remove_from_cart(request, product_id, quantity_id):
    user = request.user
    try:
        cart_item = Cart.objects.get(user_id=user.id, product_id=product_id, quantity_id=quantity_id)
    except Cart.DoesNotExist:
        pass
    else:
        cart_item.delete()

    return redirect(cart)


def wishlist(request):
    return render(request, 'wishlist.html')


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


# def add_address(request):
#     user = request.user
#     if request.method == 'POST':
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             data = form.save(commit=False)
#             if data.phone != data.phone2:  # Check if phone and phone2 are different
#                 data.user = user
#                 data.save()
#                 return redirect(select_address)
#             else:
#                 return redirect(select_address)

def add_address(request):
    user = request.user
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
        return redirect(select_address)

    else:
        return redirect(select_address)
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})


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
    cart_data = Cart.objects.filter(user_id=user.id)
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


def save_order(request, address_id):
    user = request.user
    cart_items = Cart.objects.filter(user_id=user.id)
    order = Order.objects.create(user=user, address_id=address_id)
    for cart_item in cart_items:
        order.cart_data.add(cart_item)
    cart_items.delete()

    return redirect('cart')


def order_view(request):
    return render(request, 'order_view.html')


def base(request):
    return render(request, 'base.html')

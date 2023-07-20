from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from shop.models import Category, Product

def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.filter(category=c_page, available=True)
    else:
        products_list = Product.objects.filter(available=True)

    paginator = Paginator(products_list, 6)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "category.html", {'category': c_page, 'products': products})

def proDetail(request, c_slug, product_slug):
    product = get_object_or_404(Product, category__slug=c_slug, slug=product_slug)
    return render(request, 'product.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[product.id] = cart.get(product.id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    if product.id in cart:
        del cart[product.id]
        request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        if product:
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            cart_total += subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

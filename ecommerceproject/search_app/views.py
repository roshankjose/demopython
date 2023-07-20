from django.shortcuts import render
from shop.models import Product
from django.db.models import Q

def SearchResult(request):
    query = request.GET.get('q')
    products = None

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    print("Query:", query)
    print("Products:", products)

    context = {
        'query': query,
        'products': products
    }

    return render(request, 'search.html', context=context)

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import SignupForm
from .models import *


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'core/index.html', context)


def research(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(is_sold=False)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(subCategory__name__icontains=query))

    context = {'products': products, 'query': query}
    return render(request, 'core/research.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'core/cart.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()  # GET case

    return render(request, 'core/signup.html', {
        'form': form
    })


def details(request, pk):
    item = get_object_or_404(Product, pk=pk)
    context = {'item': item}

    return render(request, 'core/details.html', context)


def login(request):
    return render(request, 'core/login.html')

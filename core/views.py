from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import SignupForm
from django.http import JsonResponse
import json, datetime
from .models import *


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ordname = order.id
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
        ordname = {'ordname': ''}

    products = Product.objects.all()
    context = {'products': products, 'cartitems': cartitems, 'ordname': ordname}

    return render(request, 'core/index.html', context)


def research(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(is_sold=False)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(subCategory__name__icontains=query))

    context = {'products': products, 'query': query}
    return render(request, 'core/research.html', context)


def details(request, pk):
    item = get_object_or_404(Product, pk=pk)
    context = {'item': item}

    return render(request, 'core/details.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'core/cart.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/index/')
    else:
        form = SignupForm()  # GET case

    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartitems = order['get_cart_items']
    context = {'form': form, 'cartitems': cartitems}
    return render(request, 'core/signup.html', context)


def login(request):
    return render(request, 'core/login.html')


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'core/checkout.html', context)


def updateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId: ', productId)
    print('Action: ', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('Item was ' + action.__str__(), safe=False)


def processOrder(request):
    transactionId = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transactionId

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        Address.objects.get_or_create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    else:
        print('User not logged in')
    print('Data: ', request.body)
    return JsonResponse('Payment Complete!', safe=False)

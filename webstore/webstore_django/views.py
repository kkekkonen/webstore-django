from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from .models import *
import json
from webstore_django.forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = auth_authenticate(request, username=username, password=raw_password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('product_list'))
        else:
            context = {
                'message': 'Invalid login! Please try again.',
            }
            return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            auth_login(request, user)
            return redirect(reverse('product_list'))
        else:
            return render(request, 'registration.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'registration.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login', )

def product(request, id):
    product = get_object_or_404(Product, pk=id)
    template = loader.get_template('product.html')
    context = {
        'product': product,
    }
    return HttpResponse(template.render(context, request))

def product_list(request):
    page = request.GET.get('page', 1)
    search_parameters = request.GET.get('search', '')
    sorting = request.GET.get('sorting', '')
    if search_parameters is not '':
        name_search = Product.objects.filter(name__contains=search_parameters)
        code_search = Product.objects.filter(code__contains=search_parameters)
        products = name_search | code_search
    else:
        products = Product.objects.all()
    if sorting is not '':
        products = products.order_by(sorting)
    else:
        products = products.order_by('name')
    paginator = Paginator(products, 4)
    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)
    template = loader.get_template('product_list.html')
    context = {
        'products': products_paginated,
        'search_parameters': search_parameters,
        'sorting': sorting,
    }
    return HttpResponse(template.render(context, request))

@staff_member_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('product', id=product.id)
        else:
            return render(request, "add_product.html", {'form': form})
    else:
        form = ProductForm()
        return render(request, "add_product.html", {'form': form})


def search_product(request, search_parameters):
    name_search = Product.objects.filter(name__unaccent__icontains=search_parameters)
    code_search = product.objects.filter(code__unaccent__icontains=search_parameters)
    search = name_search | code_search
    template = loader.get_template('search_list.html')
    context = {
        'search_list': search,
        'search_parameters': search_parameters,
    }
    return HttpResponse(template.render(context, request))

@login_required
@csrf_exempt
def remove_shopping_cart(request, id):
    template = loader.get_template('shopping_cart.html')
    product = get_object_or_404(Product, pk=id)
    shopping_cart, created = Shopping_cart.objects.get_or_create(owner=request.user, defaults={'products': '{}'})
    data = json.loads(shopping_cart.products)
    if created:
        return HttpResponse(template.render(request))
    elif str(id) in data:
        count = data[str(id)]['count'] - 1
        if count >= 1:
            data[str(id)]['count'] = count
        else:
            data.pop(str(id), None)
        shopping_cart.products = json.dumps(data)
        shopping_cart.save()
    context = {'cart': data}
    return redirect(reverse('shopping_cart'))

@login_required
@csrf_exempt
def add_shopping_cart(request, id):
    if(request.method == "POST"):
        shopping_cart, created = Shopping_cart.objects.get_or_create(owner=request.user, defaults={'products': '{}'})
        product = get_object_or_404(Product, pk=id)
        data = json.loads(shopping_cart.products)
        if str(id) in data:
            data[str(id)]['count'] = data[str(id)]['count'] + 1
        else:
            data[str(id)] = {'count': 1, 'name': product.name, 'code': product.name, 'cost': product.cost, 'id': product.id}
        shopping_cart.products = json.dumps(data)
        shopping_cart.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

def get_shopping_cart(request):
    shopping_cart, created = Shopping_cart.objects.get_or_create(owner=request.user, defaults={'products': '{}'})
    template = loader.get_template('shopping_cart.html')
    context = {
        'cart': json.loads(shopping_cart.products),
    }
    return HttpResponse(template.render(context, request))

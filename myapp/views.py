from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse
from .models import Category, Product, Client, Order
from .form import OrderForm, InterestForm, RegisterForm
from django.shortcuts import render
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def index(request):
    if request.session.has_key('username'):
        username = request.session['username']
        client = Client.objects.get(username=username)
        inCat = client.Interested_in.all()
        lastLogin = request.session['last_login']
        return render(request, 'myapp/index.html', {'client': client, 'inCat': inCat, 'last_login': lastLogin})
    else:
        request.session['url'] = 'myapp:index'
        return redirect('myapp:login')


def about(request):
    if request.session.has_key('username'):
        username = request.session['username']
        client = Client.objects.get(username=username)
        cookieValue = request.COOKIES.get('about_visits', 'default')
        if(cookieValue == 'default'):
            response = render(request, 'myapp/about.html', {'client': client, 'about_visits':'1'})
            response.set_cookie('about_visits', 1, 5*60)
        else:
            cookieValue=int(cookieValue)+1
            response = render(request, 'myapp/about.html', {'client': client, 'about_visits': cookieValue})
            response.set_cookie('about_visits', cookieValue)
        return response
    else:
        request.session['url'] = 'myapp:about'
        return redirect('myapp:login')


def detail(request, cat_id):
    if request.session.has_key('username'):
        username = request.session['username']
        client = Client.objects.get(username=username)
        category = Category.objects.filter(id=cat_id)
        products = Product.objects.filter(Category__id=cat_id)
        print(category)
        print(products)
        return render(request, 'myapp/detail.html', {'client': client, 'category': category, 'products': products})
    else:
        request.session['url'] = 'myapp:detail'
        return redirect('myapp:login')


def products(request):
    if request.session.has_key('username'):
        username = request.session['username']
        client = Client.objects.get(username=username)
        products = Product.objects.all().order_by('id')[:10]
        return render(request, 'myapp/products.html', {'client': client, 'products': products})
    else:
        request.session['url'] = 'myapp:products'
        return redirect('/myapp/login')


def place_order(request, prod_id):
    if request.session.has_key('username'):
        msg = ''
        username = request.session['username']
        prod = Product.objects.get(id=prod_id)
        products = Product.objects.all()
        client = Client.objects.get(username=username)
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                if order.num_units <= order.Product.stock:
                    order.save()
                    p = Product.objects.get(name=order.Product.name)
                    p.stock = order.Product.stock - order.num_units
                    p.save()
                    msg = 'Your order has been placed successfully.'
                else:
                    msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'myapp/orderresponse.html', {'msg': msg})
        else:
            form = OrderForm()
            return render(request, 'myapp/placeorder.html', {'client': client, 'form': form, 'msg': msg,
                                                             'products': products, 'prod': prod})
    else:
        request.session['url'] = 'myapp:place_order'
        return redirect('/myapp/login')


def productdetail(request, prod_id):
    if request.session.has_key('username'):
        product = Product.objects.get(id=prod_id)
        if request.method == 'POST':
            form = InterestForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['interested'] == 1:
                    product.interested = product.interested + form.cleaned_data['interested']
                    product.save()
            return redirect('/myapp/')
        else:
            form = InterestForm()
            return render(request, 'myapp/productdetail.html', {'form': form, 'product': product})
    else:
        request.session['url'] = 'myapp:productdetail'
        return redirect('myapp:login')


def login(request):
    if request.session.has_key('username'):
        return redirect('myapp:index')
    else:
        request.session['url'] = 'myapp:index'
        return render(request, 'myapp/login.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        useres = Client.objects.filter(username=username, password=password)
        if useres:
            user = useres.get(username=username, password=password)
            if user:
                now = datetime.datetime.now()
                lastlogin = now.strftime("%m/%d/%Y, %H:%M:%S")
                if user.is_active:
                    request.session['username'] = username
                    if not request.session.has_key('last_login'):
                        lastlogin = 'Your last login was more than one hour ago'
                        request.session['last_login'] = lastlogin
                    else:
                        request.session['last_login'] = lastlogin
                        request.session.set_expiry(3600)
                    if request.session.has_key('url'):
                        url = request.session['url']
                        return redirect(url)
                    else:
                        request.session['url'] = 'myapp:index'
                        return redirect('myapp:index')
                else:
                    request.session['url'] = 'myapp:index'
                    return redirect('myapp:register')
            else:
                return redirect('myapp:login')
        else:
            return render(request, 'myapp/invalid.html')
    else:
        return render(request, 'myapp/login.html')


def user_logout(request):
    del request.session['username']
    del request.session['url']
    return redirect('myapp:login')


def myorders(request):
    if request.session.has_key('username'):
        username = request.session['username']
        client = Client.objects.get(username=username)
        # client = Client.objects.get(id=user.id)
        myOrders = Order.objects.filter(Client__username=username)
        if myOrders:
            return render(request, 'myapp/myorders.html', {'client': client, 'myOrders': myOrders})
        else:
            return HttpResponse('You are not a registered client')
    else:
        request.session['url'] = 'myapp:myorders'
        return redirect('myapp:login')


def register(request):
    if request.session.has_key('username'):
        username = request.session['username']
        client = Client.objects.get(username=username)
        if client.is_active:
            return redirect('myapp:index')
        else:
            form = RegisterForm(request.POST)
            if request.method == 'POST':
                if form.is_valid():
                    if form.cleaned_data['register'] == True:
                        client.is_active = form.cleaned_data['register']
                        client.save()
                        return redirect('myapp:index')
                    else:
                        return redirect('myapp:register')
                else:
                    return redirect('myapp:register')
            form = RegisterForm()
            return render(request, 'myapp/register.html', {'form': form, 'client': client})
    else:
        request.session['url'] = 'myapp:index'
        return redirect('myapp:login')



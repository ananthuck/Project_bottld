from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from bottledapp.models import *
import os
from django.http import JsonResponse
from .models import Product, Cart
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def home(request):
    cat = Category.objects.all()
    pdt = Product.objects.all()
    crt = Cart.objects.all()
    return render(request, 'Home.html',  {'pdt': pdt, 'cat': cat, 'crt': crt})

def adminloginpg(request):
    return render(request, 'adminlogin.html')

def admindb(request):
    cat = Category.objects.all()
    pdt = Product.objects.all()
    return render(request, 'admindb.html', {'pdt': pdt, 'cat': cat})

    

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['uid'] = username
            return redirect('admindb')
        else:
            messages.error(request, "There is an error in logging in, please try again")
            return redirect('adminloginpg')
        
    return render(request, 'adminlogin.html')

def adminlogout(request):
    logout(request)
    messages.success(request, "You are successfully logged out!")
    return redirect('adminloginpg')

def viewproduct(request, pk=None):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(productname__icontains=query)
        return render(request, 'viewproduct.html', {'pdt': products})
    else:
        pdt = get_object_or_404(Product, id=pk)
        return render(request, 'viewproduct.html', {'pdt': pdt})

def addproduct(request):
    categories = Category.objects.all()
    return render(request, 'addprdt.html', {'categories': categories})

def addcategory(request):
    return render(request, 'addcat.html')

def addcategoryf(request):
    if request.method == 'POST':
        pcategory = request.POST['productcategory']
        addctgry = Category(productcategory=pcategory)
        addctgry.save()
        return redirect('addcategory')
    
def addproductf(request):
    if request.method == 'POST':
        pname = request.POST['productname']
        pdescription = request.POST['description']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        pprice = request.POST['price']
        image = request.FILES.get('image')
        if image is not None:
            addprdt = Product(productname=pname, price=pprice, description=pdescription, category=category, image=image)
            addprdt.save()
        return redirect('addproduct')
    
def deletecat(request, pk):
    udatas=Category.objects.get(id=pk)
    udatas.delete()
    return redirect('admindb')
    
def edit(request, pk):
    udata=Product.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request, 'editprdt.html', {'udata':udata, 'categories': categories})

def editf(request, pk):
    if request.method == 'POST':
        productdata = Product.objects.get(id=pk)
        productdata.productname = request.POST.get('productname')
        productdata.description = request.POST.get('description')
        category_id = request.POST['category']
        productdata.category = Category.objects.get(id=category_id)
        productdata.price = request.POST.get('price')
        uploaded_file = request.FILES.get('image')
        if uploaded_file:
            if os.path.exists(productdata.image.path):
                os.remove(productdata.image.path)
            productdata.image=uploaded_file
        productdata.save()
        return redirect('admindb')
    return render(request, 'editprdt.html')


def deletepdt(request, pk):
    udatas=Product.objects.get(id=pk)
    if udatas.image is not None:
        os.remove(udatas.image.path)
    udatas.delete()
    return redirect('admindb')

def search_product(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(productname__icontains=query)
        results = [{'id': p.id, 'name': p.productname} for p in products]
    else:
        results = []
    return JsonResponse(results, safe=False)

@csrf_exempt
def contact_mail(request):
    if request.method == 'POST':
        name=request.POST.get('Name')
        email=request.POST.get('Email')
        message=request.POST.get('Message')
        print(name, email, message)
        send_mail(
            subject=f"New Contact Form Submission from {name}",
            message=message,
            from_email='noreply@example.com',
            recipient_list=['ananthuckofficial@gmail.com'],
        )
        
        return redirect('home')
    return render(request, 'Home.html')

def userlogin(request):
    return render(request, 'userlogin.html')

def userreg(request):
    return render(request, 'userreg.html')

def addtocart(request):
    if request.method == 'POST':
        pid = request.POST['id']
        pquantity = int(request.POST['quantity'])
        product = get_object_or_404(Product, id=pid)
        cart_item = Cart.objects.filter(product=product).first()
        if cart_item:
            cart_item.quantity += pquantity
            cart_item.save()
        else:
            Cart.objects.create(product=product, quantity=pquantity)
         
        return redirect('home')
        
    return render(request, 'Home.html')

def deleteitem(request, pk):
    citem=Cart.objects.get(id=pk)
    citem.delete()
    return redirect('home') 


def update_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('id')
        action = request.POST.get('action')
        
        if not cart_item_id or not action:
            return JsonResponse({'error': 'Invalid request parameters'}, status=400)
        
        try:
            cart_item = Cart.objects.get(id=cart_item_id)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
        cart_item.save()
        
        return JsonResponse({'quantity': cart_item.quantity, 'total_price': cart_item.total_price})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
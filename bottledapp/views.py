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
from twilio.rest import Client
import random
from django.views.decorators.cache import cache_control


# Create your views here.

# TWILIO_ACCOUNT_SID = "ACe40ee2636521cecbe7fc0673ee4b9cc7"
# TWILIO_AUTH_TOKEN = "adec3667f071626c92cd0f19d4fa207a"

# c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


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
    udt = Userlogin.objects.all()
    return render(request, 'admindb.html', {'pdt': pdt, 'cat': cat, 'udt':udt})

    

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
        crt = Cart.objects.all()
        return render(request, 'viewproduct.html', {'pdt': products, 'crt':crt})
    else:
        pdt = get_object_or_404(Product, id=pk)
        crt = Cart.objects.all()
        return render(request, 'viewproduct.html', {'pdt': pdt, 'crt':crt })

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

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp(phone_number, otp):
    client = Client('ACe40ee2636521cecbe7fc0673ee4b9cc7', 'adec3667f071626c92cd0f19d4fa207a')
    client.messages.create(
        body=f'Your OTP is: {otp}',
        from_='+12067598555',
        to=f'+91{phone_number}' )
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def user_reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        request.session['temp_phone_number'] = phone_number
        otp = generate_otp()
        send_otp(phone_number, otp)
        request.session['otp'] = otp

        user, created = Userlogin.objects.get_or_create(name=name,sex=sex,email=email,mobile_number=phone_number,password=password,)
        return redirect('verify_otp')
    
    return render(request, 'userreg.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            phone_number = request.session.get('temp_phone_number')
            user_login, created = Userlogin.objects.get_or_create(mobile_number=phone_number)
            user_login.otp_verified = True
            user_login.save()
            return redirect('userlogin')
        else:
            return HttpResponse("Invalid OTP. Please try again.")

    return render(request, 'Verifyotp.html')

def deleteuser(request, pk):
    udatas=Userlogin.objects.get(id=pk)
    udatas.delete()
    return redirect('admindb')

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
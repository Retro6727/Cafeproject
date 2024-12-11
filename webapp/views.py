from urllib import request
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Food, Cart, Customer, OrderItem
from .forms import registrationForm, AuthenticationForm, AddressForm,UserAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views import View
import random
import uuid
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer

# Create your views here.
def show(request):
    category = Category.objects.all()
    product = Food.objects.all()
    print(category)
    context = {}
    context['category'] = category
    context['product'] = product
    return render(request, 'index.html', context)

def cat_view(request, id):
    category = Category.objects.all()
    product = Food.objects.filter(category=id)
    context = {}
    context['category']=category
    context['product']=product
    return render(request,"index.html",context)

def addprod(request,id):
    product=Food.objects.filter(id=id)
    print(product)
    context={'product':product}
    return render(request,"menu.html",context)

# User Registration Form

def register(request):
    if request.method == "POST":
        uform = registrationForm(request.POST)
        if uform.is_valid():
            uform.save()
            return redirect('thanks')
        
    else:
        uform = registrationForm()
    return render(request, 'register.html', {'forms': uform})

# Login Form
def login_details(request):
    if request.method == "POST":
        lform = UserAuthenticationForm(request.POST)
        username=request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'logform': lform,'msg':'wrong credentials!!!'})
    else:
        lform = UserAuthenticationForm()
    return render(request, 'login.html', {'logform': lform})
        
# Logout Form
def user_logout(request):
    logout(request)
    return redirect('home')

# Thank you messsage
def tym(request):
    return render(request, 'thankyou.html')

# Price Range functionality
def range(request):
    max=request.GET['maxprice']
    min=request.GET['minprice']
    print(max)
    print(min)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    p=Food.objects.filter(q1 & q2)
    context={}
    context['product']=p
    return render(request, "index.html", context)


# Add to cart functionality
@login_required(login_url='login_details')
def addcart(request, pid):
    print("User ID:", request.user.id)
    print("Authenticated:", request.user.is_authenticated)

    if request.user.is_authenticated:
        userid = request.user.id
        u = User.objects.filter(id=userid)
        p = Food.objects.filter(id=pid)

       

        q1 = Q(uid=u[0])
        q2 = Q(pid=p[0])
        
        c = Cart.objects.filter(q1 & q2)
        print(c)
        context = {'product': p}
        if c.exists():
            context['msg'] = "Product already exists in the cart !!"
            return render(request, 'menu.html', context)
        else:
            c = Cart.objects.create(uid=u[0], pid=p[0])
            context['success'] = "Product Added Successfully to Cart !!"
            return render(request, 'menu.html', context)
    else:
        print("User not authenticated, redirecting to login")

    
# Cart page
def viewCart(request):
    userid = request.user.id
    cart_data = Cart.objects.filter(uid=userid)
    total_price=0
    for x in cart_data:
        total_price = total_price + x.pid.price * x.qty
    print(total_price)
    context={'data':cart_data,'total':total_price}
    return render(request, 'cart.html', context)

# Remove food item from cart
def remove(request,cid):
    removeItem = Cart.objects.filter(id=cid)
    print(removeItem)
    removeItem.delete()
    return redirect('/viewcart')

# Update Quantity
def updateqty(request, qv, cid):
    cart_data=Cart.objects.filter(id=cid)
    print(cart_data)
    if qv=='1':
        total_quantity=cart_data[0].qty+1
        cart_data.update(qty=total_quantity)
    elif qv=='0':
        total_quantity=cart_data[0].qty-1
        cart_data.update(qty=total_quantity)
    return redirect('/viewcart')
   
def checkout(request):
    userid = request.user
    cart_items = Cart.objects.filter(uid=userid)
    print(cart_items)
    total_price=0
    delivery_charge=50
    for x in cart_items:
        total_price= total_price+x.pid.price*x.qty
    final_price=delivery_charge + total_price
    customer=Customer.objects.filter(user=request.user)
    context = {
        'data': cart_items,
        'delivery_charges': delivery_charge,
        'total': total_price,
        'final': final_price,
        'forms': AddressForm(),
        'customer_details':customer
    }
    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECIEVER_EMAIL,
        'amount': final_price,
        'item_name': 'Food',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"https://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess')}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",


    }
    paypal_payment=PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        'data': cart_items,
        'delivery_charges': delivery_charge,
        'total': total_price,
        'final': final_price,
        'forms': AddressForm(),
        'customer_details':customer,
        'paypal':paypal_payment
    }
   
            
    return render(request, 'checkout.html',context)

def customer_detail(request):
    if request.method == "POST":
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('home')

        else:
            context = {'address_form': address_form}
            return render(request, 'address.html', context)
    else:
        address_form = AddressForm()
        context = {'address_form': address_form}
        return render(request, 'address.html', context)
    

def paymentsuccessful(request):
    return render(request, 'paymentsuccessful.html')
def paymentfailed(request):
    return render(request, 'paymentfailed.html')

def menu_view(request):
    products = Food.objects.all()
    random_products = random.sample(list(products), k = min(4, len(products)))
    return render(request, 'menu.html', {'products': products, 'random_products': random_products})

    
#def paynow(request):
def placeorder(request):
    userid = request.user.id
    cart_items = Cart.objects.filter(uid=userid)
    total = 0    
    current_order_items = []  

    for item in cart_items:
        item_total = item.pid.price * item.qty
        total += item_total
        order_item = OrderItem.objects.create(
            items=item.pid,
            user=item.uid,
            total_price=item_total,
            quantity=item.qty,
            status="PENDING",
            payment_method="COD",
            payment_status="PENDING"
        )
        current_order_items.append(order_item) 
        item.delete()

    payment_success = True  
    
    if payment_success:
        OrderItem.objects.filter(user=request.user.id, payment_status="PENDING").update(payment_status="SUCCESS")
    else:
        OrderItem.objects.filter(user=request.user.id, payment_status="PENDING").update(payment_status="FAILED")


    context = {
        'data': current_order_items,
        'total': total
    }

    return render(request, 'placeorder.html', context)


# def menu(request):
#     products = Food.objects.all()
#     random_products = random.sample(list(products), min(4, len(products)))  # Get up to 4 random items
#     context = {
#         'product': products,
#         'random_products': random_products,
#     }
#     return render(request, 'menu.html', context)


class crud_api(APIView):
    def post(self, request):
        cust_data = request.data
        print(cust_data)
        serializer = CustomerSerializer(data=cust_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success" : "data is successfully saved"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id=request.data.get('id', None)
        print(id)
        if id:
            try:
                cust_data = Customer.objects.get(id=id)
                serializer=CustomerSerializer(cust_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({"Error": "id is not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            cust_data = Customer.objects.all()
            print(cust_data)
            serializer = CustomerSerializer(cust_data, many=True)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request):
        update_data=request.data
        print(update_data)
        id=request.data.get("id")
        if id:
             cust_data=Customer.objects.get(id=id)
             print(cust_data)
             serializer=CustomerSerializer(cust_data,update_data,partial=True)
             if serializer.is_valid():
                  serializer.save()
                  return Response({"Success":"Successfully updated"},status=status.HTTP_200_OK)
             
    def delete(self, request):
        id=request.data.get("id")
        cust_data=Customer.objects.get(id=id)
        if id:
             cust_data.delete()
             return Response({"success":"successsfully deleted"},status=status.HTTP_200_OK)
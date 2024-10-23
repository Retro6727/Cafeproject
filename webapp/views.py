from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Food
from .forms import registrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
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
def login(request):
    if request.method == "POST":
        lform = AuthenticationForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
    else:
        lform = AuthenticationForm()
    return render(request, 'login.html', {'logform': lform})

# Logout Form
def user_logout(request):
    logout(request)
    return redirect('home')

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
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Food
from .forms import registrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
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
            return redirect('thankyou')
        
    else:
        uform = registrationForm()
    return render(request, 'register.html', {'forms': uform})
    
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
    
def user_logout(request):
    logout(request)
    return redirect('home')

def tym(request):
    return render(request, 'thankyou.html')
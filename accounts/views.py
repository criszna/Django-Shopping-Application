from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from store.models import Customer
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer=Customer()
            customer.user=user
            customer.email=request.POST.get('email')
            customer.name = request.POST.get('username')
            customer.save()
            login(request,user)
            return redirect('store:store')
    else:
        form = UserCreationForm()
    return render(request,'accounts/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if 'next'in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('store:store')
    else:
        form = AuthenticationForm()
        print("display form")
    return render(request,'accounts/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('store:store')

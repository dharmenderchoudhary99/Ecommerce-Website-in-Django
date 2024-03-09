from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from .models import Profile



def login_page(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)

        if user_obj[0].profile.is_email_verified():
            messages.warning(request, 'Your Account is not verified')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request,user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/login.html')

def register_page(request):
    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')



        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already takes')
            return HttpResponseRedirect(request.path_info)
        
        user_obj= User.objects.create(first_name=first_name,last_name=last_name,email=email,username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your email')
        return HttpResponseRedirect(request.path_info)
    


    return render(request,'accounts/register.html')

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid Email Token")
    
def cart(request):
    context = {'cart': Cart.objects.get(is_paid = False,user= request.user)}

    if request.method == 'POST':
        return render(request,'accounts/cart.html'. context)
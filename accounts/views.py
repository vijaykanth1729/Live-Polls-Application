from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next','polls:list')
            return redirect(redirect_url)
        else:
            messages.success(request, 'Bad Username or password')
    return render(request, 'accounts/login.html')
@login_required
def logout_user(request):
    logout(request)
    return redirect('polls:home')

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            human = True
            user = User.objects.create_user(username=username,email=email, password=password)
            messages.success(request,"Thanks for registering with us {}".format(user.username))
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html',{'form':form})



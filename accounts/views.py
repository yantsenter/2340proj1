from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy

from django.contrib import messages

# Create your views here.
from .forms import CustomUserCreationForm, CustomErrorList, UpdatePasswordForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

def update_password_view(request):
    if request.method == "POST":
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            new_password = form.cleaned_data["new_password"]

            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully. You can now log in with your new password.")
                return redirect("accounts.login")  # Redirect to login page
            except User.DoesNotExist:
                messages.error(request, "User with this username does not exist.")

    else:
        form = UpdatePasswordForm()

    return render(request, "accounts/password_reset.html", {"form": form})
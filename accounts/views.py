from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, PasswordResetView
from .forms import RegistrationForm, ProfileForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.is_active = True  # Kích hoạt tài khoản ngay lập tức
                    user.save()
                    
                    # Đăng nhập người dùng ngay sau khi đăng ký
                    login(request, user)
                    messages.success(request, 'Registration successful.')
                    return redirect('home')
            except IntegrityError:
                messages.error(request, 'An error occurred during registration. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'  # Đặt template email

@login_required
def profile_view(request):
    profile = request.user.profile  # Truy cập profile của người dùng hiện tại
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Chuyển hướng người dùng đến trang profile
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Hoặc trang bạn muốn chuyển hướng sau khi đăng nhập
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

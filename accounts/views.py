<<<<<<< HEAD
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
=======
from .forms import ProfileForm, RegistrationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_str
from .forms import RegistrationForm


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('login')




def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    })
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            user.save()
            
            send_verification_email(user, request)
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})

# Đăng nhập
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Tên template muốn sử dụng

# Đăng xuất
class CustomLogoutView(LogoutView):
    next_page = '/'  # Trang đích sau khi đăng xuất (nếu cần)


@login_required
def profile_view(request):
    profile = request.user.profile  # Truy cập profile của người dùng hiện tại
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Chuyển hướng người dùng đến trang profile
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

>>>>>>> 97ee8979c26f5f129f58b20f34ac71188cb18c3b

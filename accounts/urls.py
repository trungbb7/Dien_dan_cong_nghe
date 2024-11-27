<<<<<<< HEAD
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile_view, edit_profile, login_view
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [

    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    
    path('register/', views.register, name="register"),
    
    path('login/', login_view, name='login'),
    
    # Đường dẫn cho chức năng quên mật khẩu
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile_view, edit_profile
urlpatterns = [

    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    
    path('register/', views.register, name="register"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('login/',auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    
    # Đường dẫn cho chức năng quên mật khẩu
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]
>>>>>>> 97ee8979c26f5f129f58b20f34ac71188cb18c3b

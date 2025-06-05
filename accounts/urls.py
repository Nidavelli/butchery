from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Profile view
    path('profile/', views.profile, name='profile'),
    
    # Password change views - override the success_url
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        success_url='/accounts/password-change-done/'
    ), name='password_change'),
    
    path('password-change-done/', views.password_change_done, name='password_change_done'),
    
    # Include Django's default auth URLs for login/logout/password reset
    # but exclude the password change URLs we defined above
    path('', include('django.contrib.auth.urls')),
]


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
import re

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'})
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Enter a valid email address.')
            
        return email

@login_required
def profile(request):
    """
    View for displaying and updating user profile information.
    GET request displays the current profile.
    POST request updates the profile with submitted data.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Get order history for display in profile
    from shop.models import Order
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]  # Get 5 most recent orders
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'recent_orders': orders
    })

def password_change_done(request):
    """Custom view for password change success to add a success message"""
    messages.success(request, 'Your password has been changed successfully.')
    return redirect('accounts:profile')

from django.shortcuts import render

# Create your views here.

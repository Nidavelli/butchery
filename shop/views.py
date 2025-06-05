from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.exceptions import ValidationError
import json
import re

def landing_page(request):
    """Landing page view with featured products"""
    try:
        # Get featured products (limit to 6 for the landing page)
        featured_products = Product.objects.filter(available=True)[:6]
        
        # Get cart count for the template
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
        
        context = {
            'featured_products': featured_products,
            'cart_count': cart_count,
        }
        
        return render(request, 'shop/landing.html', context)
    except Exception as e:
        messages.error(request, f"Error loading landing page: {str(e)}")
        return render(request, 'shop/landing.html', {'featured_products': [], 'cart_count': 0})

def product_list(request):
   products = Product.objects.filter(available=True)
   return render(request, 'shop/product_list.html', {'products':products})

def product_detail(request, pk):
   product = get_object_or_404(Product, pk=pk)
   return render(request, 'shop/product_detail.html', {'product':product})
  
@login_required
def place_order(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        
        # Check if product is available
        if not product.available:
            messages.error(request, "This product is currently out of stock.")
            return redirect('product_detail', pk=pk)
            
        if request.method == "POST":
            quantity = int(request.POST.get("quantity", 1))
            
            # Validate quantity
            if quantity < 1:
                messages.error(request, "Quantity must be at least 1.")
                return redirect('product_detail', pk=pk)
                
            # Create the order
            Order.objects.create(
                user=request.user, 
                product=product, 
                quantity=quantity
            )
            
            messages.success(request, f"Order for {quantity} x {product.name} placed successfully!")
            return redirect('order_history')
        
        # GET request: show the product detail page
        return redirect('product_detail', pk=pk)
    except Exception as e:
        messages.error(request, f"Error placing order: {str(e)}")
        return redirect('product_list')   
@login_required
def order_history(request):
    try:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'shop/order_history.html', {'orders': orders})
    except Exception as e:
        messages.error(request, f"Error retrieving order history: {str(e)}")
        return redirect('product_list')
   
@require_POST
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product is available
        if not product.available:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'This product is currently out of stock.'
                }, status=400)
            messages.error(request, "This product is currently out of stock.")
            return redirect('product_detail', pk=product_id)
        
        # Get quantity from POST data
        quantity = int(request.POST.get('quantity', 1))
        
        # Update cart in session
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        
        # Calculate cart count
        cart_count = sum(cart.values())
        
        # Success message
        success_message = f"Added {quantity} x {product.name} to cart."
        
        # Handle AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': success_message,
                'cart_count': cart_count,
            })
        
        # Handle regular request
        messages.success(request, success_message)
        return redirect('product_list')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        messages.error(request, f"Error adding product to cart: {str(e)}")
        return redirect('product_list')
   
def view_cart(request):
   cart = request.session.get('cart', {})
   cart_items = []
   total_price = 0
   
   for product_id, quantity in cart.items():
      try:
          product = get_object_or_404(Product, id=product_id)
          item_total = product.price * quantity
          cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
          total_price += item_total
      except:
          # If product not found, remove it from cart
          cart.pop(str(product_id), None)
          request.session['cart'] = cart
          messages.warning(request, f"A product in your cart is no longer available and has been removed.")
   
   # Get cart count for the template
   cart_count = sum(cart.values())
   
   return render(request, 'shop/cart.html', {
       'cart_items': cart_items, 
       'total_price': total_price,
       'cart_count': cart_count
   })
   
def remove_from_cart(request, product_id):
    try:
        # Get current cart
        cart = request.session.get('cart', {})
        
        # Get product info for message (if needed)
        product_name = "Item"
        try:
            product = get_object_or_404(Product, id=product_id)
            product_name = product.name
        except:
            pass
        
        # Remove from cart
        if str(product_id) in cart:
            cart.pop(str(product_id), None)
            request.session['cart'] = cart
            success_message = f"{product_name} removed from cart."
            
            # Calculate new cart count
            cart_count = sum(cart.values())
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': success_message,
                    'cart_count': cart_count,
                })
            
            # Handle regular request
            messages.info(request, success_message)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Item not found in cart.'
                }, status=400)
            messages.warning(request, "Item not found in cart.")
        
        return redirect('view_cart')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        messages.error(request, f"Error removing product from cart: {str(e)}")
        return redirect('view_cart')
   
@login_required
def checkout(request):
   cart = request.session.get('cart', {})
   if not cart:
      messages.warning(request, "Your cart is empty.")
      return redirect('product_list')
   for product_id, quantity in cart.items():
      product = get_object_or_404(Product, id=product_id)
   Order.objects.create(user=request.user, product=product, quantity=quantity)
   request.session['cart'] = {}
   messages.success(request, "Order placed successfully!")
   return redirect('order_history')

# Custom UserCreationForm with email field and terms acceptance
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'})
    )
    terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must accept the Terms of Service and Privacy Policy'}
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'terms')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling to built-in fields
        self.fields['username'].widget.attrs.update({
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-accent-500 focus:border-accent-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Enter a valid email address.')
            
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # Custom password validation
        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        if password1.isdigit():
            raise ValidationError('Password cannot be entirely numeric.')
        
        # Check for at least one digit and one letter
        if not (any(char.isdigit() for char in password1) and any(char.isalpha() for char in password1)):
            raise ValidationError('Password must contain both letters and numbers.')
            
        return password1
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# SignUpView
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully. You can now log in.')
        return response
    
    def form_invalid(self, form):
        return super().form_invalid(form)

# Get cart count AJAX view
def get_cart_count(request):
    try:
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
        return JsonResponse({
            'status': 'success',
            'cart_count': cart_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# Update cart quantity AJAX view
@require_POST
def update_cart_quantity(request, product_id):
    try:
        # Get data from request
        data = json.loads(request.body) if request.body else request.POST
        quantity = int(data.get('quantity', 1))
        
        # Validate quantity
        if quantity < 1:
            return JsonResponse({
                'status': 'error',
                'message': 'Quantity must be at least 1.'
            }, status=400)
        
        # Get product
        product = get_object_or_404(Product, id=product_id)
        
        # Update cart
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        
        # Calculate item total and cart count
        item_total = product.price * quantity
        cart_count = sum(cart.values())
        
        # Calculate cart total
        total_price = 0
        for prod_id, qty in cart.items():
            try:
                prod = get_object_or_404(Product, id=prod_id)
                total_price += prod.price * qty
            except:
                pass
        
        return JsonResponse({
            'status': 'success',
            'message': f"Updated quantity for {product.name}.",
            'item_total': item_total,
            'cart_count': cart_count,
            'total_price': total_price
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# Create your views here.

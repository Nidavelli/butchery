from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from shop.models import Product, Order, Category
from django.contrib.auth.models import User
from .forms import ProductForm, ProductSearchForm, ProductExportForm
from .utils import (
    export_products_csv, export_products_excel, export_products_pdf, 
    export_products_odt, search_products, get_export_requirements
)

@staff_member_required
def dashboard_home(request):
    """Main dashboard view with key metrics"""
    # Get date range for statistics
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic counts
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    
    # Recent orders
    recent_orders = Order.objects.select_related('user', 'product').order_by('-created_at')[:10]
    
    # Sales statistics
    total_revenue = Order.objects.aggregate(
        total=Sum('product__price')
    )['total'] or 0
    
    weekly_orders = Order.objects.filter(created_at__gte=week_ago).count()
    monthly_orders = Order.objects.filter(created_at__gte=month_ago).count()
    
    # Product statistics
    low_stock_products = Product.objects.filter(available=False).count()
    
    # Top selling products
    top_products = Product.objects.annotate(
        order_count=Count('order')
    ).order_by('-order_count')[:5]
    
    # Category distribution
    category_stats = Category.objects.annotate(
        product_count=Count('product'),
        order_count=Count('product__order')
    ).order_by('-order_count')
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_categories': total_categories,
        'total_revenue': total_revenue,
        'weekly_orders': weekly_orders,
        'monthly_orders': monthly_orders,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'category_stats': category_stats,
    }
    
    return render(request, 'dashboard/home.html', context)

@staff_member_required
def sales_analytics(request):
    """Detailed sales analytics view"""
    # Daily sales for the last 30 days
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    daily_sales = []
    for i in range(30):
        date = today - timedelta(days=i)
        orders = Order.objects.filter(created_at__date=date)
        revenue = sum(order.quantity * order.product.price for order in orders)
        daily_sales.append({
            'date': date.strftime('%Y-%m-%d'),
            'orders': orders.count(),
            'revenue': float(revenue)
        })
    
    daily_sales.reverse()
    
    # Order status distribution
    delivered_orders = Order.objects.filter(is_delivered=True).count()
    pending_orders = Order.objects.filter(is_delivered=False).count()
    
    context = {
        'daily_sales': daily_sales,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'total_orders': delivered_orders + pending_orders,
    }
    
    return render(request, 'dashboard/sales_analytics.html', context)

@staff_member_required
def product_management(request):
    """Product management dashboard"""
    products = Product.objects.select_related('category').annotate(
        order_count=Count('order')
    ).order_by('-order_count')

    # Initialize forms
    export_form = ProductExportForm(request.GET or None)
    search_form = ProductSearchForm(request.GET or None)

    # Handle product search
    products = search_products(products, search_form)

    # Handle product export
    if request.method == "GET" and 'export' in request.GET:
        if export_form.is_valid():
            format = export_form.cleaned_data.get('format')
            include_images = export_form.cleaned_data.get('include_images')

            if format == 'csv':
                return export_products_csv(products, include_images=include_images)
            elif format == 'pdf':
                return export_products_pdf(products, include_images=include_images)
            elif format == 'xlsx':
                return export_products_excel(products, include_images=include_images)
            elif format == 'odt':
                return export_products_odt(products, include_images=include_images)

    # Handle pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'export_form': export_form,
        'search_form': search_form,
        'export_requirements': get_export_requirements(),
    }
    
    return render(request, 'dashboard/product_management.html', context)

@staff_member_required
def order_management(request):
    """Order management dashboard"""
    orders = Order.objects.select_related('user', 'product').order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status == 'delivered':
        orders = orders.filter(is_delivered=True)
    elif status == 'pending':
        orders = orders.filter(is_delivered=False)
    
    context = {
        'orders': orders,
        'current_status': status,
    }
    
    return render(request, 'dashboard/order_management.html', context)

@staff_member_required
def api_dashboard_stats(request):
    """API endpoint for dashboard statistics"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Calculate statistics
    stats = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'weekly_orders': Order.objects.filter(created_at__gte=week_ago).count(),
        'pending_orders': Order.objects.filter(is_delivered=False).count(),
        'total_revenue': float(sum(
            order.quantity * order.product.price 
            for order in Order.objects.select_related('product')
        )),
    }
    
    return JsonResponse(stats)

# Product CRUD Views
@staff_member_required
def product_create(request):
    """Create a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" has been created successfully!')
            return redirect('dashboard:product_management')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product',
        'action': 'Create'
    }
    
    return render(request, 'dashboard/product_form.html', context)

@staff_member_required
def product_detail(request, pk):
    """View product details"""
    product = get_object_or_404(Product, pk=pk)
    
    # Get related orders
    orders = Order.objects.filter(product=product).select_related('user').order_by('-created_at')[:10]
    
    context = {
        'product': product,
        'orders': orders,
    }
    
    return render(request, 'dashboard/product_detail.html', context)

@staff_member_required
def product_update(request, pk):
    """Update an existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully!')
            return redirect('dashboard:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'action': 'Update'
    }
    
    return render(request, 'dashboard/product_form.html', context)

@staff_member_required
def product_delete(request, pk):
    """Delete a product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('dashboard:product_management')
    
    context = {
        'product': product,
    }
    
    return render(request, 'dashboard/product_delete.html', context)

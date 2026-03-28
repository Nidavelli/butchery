from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import Category, Product, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']
    search_fields = ['name']
    list_per_page = 20
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Products'
    product_count.admin_order_field = 'product_count'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(product_count=Count('product'))
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'order_count', 'image_preview']
    list_filter = ['category', 'available', 'price']
    search_fields = ['name', 'description']
    list_editable = ['price', 'available']
    list_per_page = 25
    readonly_fields = ['image_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'available')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    def order_count(self, obj):
        return obj.order_set.count()
    order_count.short_description = 'Orders'
    order_count.admin_order_field = 'order_count'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(order_count=Count('order'))
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_price', 'created_at', 'delivery_status']
    list_filter = ['is_delivered', 'created_at', 'product__category']
    search_fields = ['user__username', 'user__email', 'product__name']
    date_hierarchy = 'created_at'
    list_per_page = 30
    readonly_fields = ['total_price']
    
    def total_price(self, obj):
        return f"${obj.quantity * obj.product.price:.2f}"
    total_price.short_description = 'Total'
    
    def delivery_status(self, obj):
        if obj.is_delivered:
            return format_html('<span style="color: green;">✓ Delivered</span>')
        return format_html('<span style="color: red;">✗ Pending</span>')
    delivery_status.short_description = 'Status'
    delivery_status.admin_order_field = 'is_delivered'
    
    actions = ['mark_as_delivered', 'mark_as_pending']
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(is_delivered=True)
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(is_delivered=False)
        self.message_user(request, f'{updated} orders marked as pending.')
    mark_as_pending.short_description = "Mark selected orders as pending"

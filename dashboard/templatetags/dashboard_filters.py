from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divides the value by the argument."""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary."""
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return None

@register.filter
def get_total_revenue(orders):
    """Calculate total revenue from orders."""
    try:
        total = 0
        for order in orders:
            total += float(order.quantity) * float(order.product.price)
        return total
    except:
        return 0

@register.filter
def get_avg_quantity(orders):
    """Calculate average quantity per order."""
    try:
        if not orders:
            return 0
        total_quantity = sum(order.quantity for order in orders)
        return total_quantity / len(orders)
    except:
        return 0


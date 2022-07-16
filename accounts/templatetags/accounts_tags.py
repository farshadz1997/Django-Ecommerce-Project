from django import template

register = template.Library()

@register.simple_tag(name="total_item_price")
def calculate_total_product_price(qty, price):
    return str(qty * price)
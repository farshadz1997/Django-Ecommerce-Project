from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_num_of_product(context):
    basket = context['basket']
    product = context['product']
    if str(product.id) in basket.basket.keys():
        return str(basket.basket[str(product.id)]['qty'])
    else:
        return '1'
        
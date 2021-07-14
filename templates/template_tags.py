from decimal import Decimal

from django import template


register = template.Library()

@register.filter
def valor_descontado(value, arg):
    """Aplica desconto no valor total"""
    desconto = (value / 100) * arg
    valor = value - round(desconto, 2)
    return round(valor, 2)

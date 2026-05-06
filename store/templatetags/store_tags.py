from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Permite acceder a diccionarios con variable como clave en templates."""
    if dictionary is None:
        return 0
    return dictionary.get(key, 0)


@register.filter
def multiply(value, arg):
    """Multiplica dos valores."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def currency(value):
    """Formatea como moneda."""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"


@register.simple_tag
def stars_range(n):
    """Genera rango para renderizar estrellas."""
    return range(1, 6)

# -*- coding: utf-8 -*-
from django.conf import settings

from currencies import models
from django import template

register = template.Library()

class PriceNode(template.Node):
    currency_code = None

    def __init__(self, amount, currency_code):
        self.amount         = template.Variable(amount)
        if currency_code:
            self.currency_code  = template.Variable(currency_code)

    def render(self, context):
        try:
            amount = self.amount.resolve(context)
            if self.currency_code:
                currency_code = self.currency_code.resolve(context)
            else:
                currency_code  = models.DEFAULT_CURRENCY
            return '%g' % models.currency_converter(amount, currency_code, context['currency'])
        except template.VariableDoesNotExist:
            return 'N/A'

@register.tag(name="price")
def price(parser, token):
    """ usage format: {% price <amount> [source_currency] %}
        converts from source currency to context currency. If source currency omitted,
        settings default currency used
    """
    args = token.split_contents()
    tag_name = args[0]
    try:
        amount = args[1]
    except IndexError:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % tag_name
    try:
        currency_code = args[2]
    except:
        currency_code = None
    return PriceNode(amount, currency_code)



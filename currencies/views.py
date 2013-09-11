# -*- coding: utf-8 -*-
from django import http, shortcuts
import models

def set_currency(request):
    currency_code = request.REQUEST.get('currency')

    currency = shortcuts.get_object_or_404(models.Currency, code=currency_code)

    next = request.REQUEST.get('next') or request.META.get('HTTP_REFERER', None) or '/'
    response = http.HttpResponseRedirect(next)

    if currency_code:
        if hasattr(request, 'session'):
            request.session['currency'] = currency_code
        else:
            response.set_cookie('currency', currency_code)
    return response


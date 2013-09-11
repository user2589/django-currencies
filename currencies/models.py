# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import caching.base

from countries import models as countries

DEFAULT_CURRENCY = getattr(settings, 'DEFAULT_CURRENCY', 'USD')
CURRENCY_COOKIE_NAME = getattr(settings, 'CURRENCY_COOKIE_NAME', 'django_currency')

class Currency(caching.base.CachingMixin, models.Model):
    code    = models.CharField(_('code'), max_length=3, primary_key=True,
                    help_text=_('ISO 4217 currency code'))
    name    = models.CharField(max_length=40)
    symbol  = models.CharField(_('symbol'), max_length=3, null=True, blank=True)
    factor  = models.DecimalField(_('factor'), max_digits=10, decimal_places=4, default=0,
                    help_text=_('Specifies the difference of the currency to default one.'))
    is_active = models.BooleanField(_('active'), default=True,
                    help_text=_('The currency will be available.'))
    last_update  = models.DateTimeField(editable=False, auto_now=True,
                    help_text=_('Date of last exchange rate update.'))

    objects = caching.base.CachingManager()

    class Meta:
        db_table = 'currencies'
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')
        ordering = ('code',)

    def __unicode__(self):
        return self.symbol or self.code


class CountryCurrency(caching.base.CachingMixin, models.Model):
    country  = models.ForeignKey(countries.Country, unique=True)
    currency = models.ForeignKey(Currency)

    objects = caching.base.CachingManager()

    class Meta:
        ordering = ('country',)
        verbose_name = _('Country currency')
        verbose_name_plural = _('Countries currency')

    def __unicode__(self):
        return u"%s: %s"%(self.country, self.currency)


def currency_converter(amount, source_currency_code=DEFAULT_CURRENCY, target_currency_code=DEFAULT_CURRENCY):
    if target_currency_code == source_currency_code:
        return float(amount) #bevare of strings

    if isinstance(source_currency_code, Currency):
        source_currency = source_currency_code #Currency instance passed instead of code
    else:
        source_currency, created = Currency.objects.get_or_create(code=source_currency_code)
        if created:
            update_rate(source_currency)

    if isinstance(target_currency_code, Currency):
        target_currency = target_currency_code
    else:
        target_currency, created = Currency.objects.get_or_create(code=target_currency_code)
        if created:
            update_rate(target_currency)

    return round(float(amount)*float(target_currency.factor)/float(source_currency.factor), 2)

def update_rate(currency):
    if currency.code == DEFAULT_CURRENCY:
        currency.factor = 1
    else:
        factor = 0
        try:
            import urllib
            response = urllib.urlopen('http://download.finance.yahoo.com/d/quotes.csv?s=%s%s=X&f=l1'%(DEFAULT_CURRENCY, currency.code))
            response_text = response.read(20)
            factor = response_text
        except IOError:
            pass
        if float(factor) == 0:
            currency.is_active = False
        else:
            currency.factor = factor
    currency.save()

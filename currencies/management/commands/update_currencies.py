# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from currencies import models
from optparse import make_option

class Command(BaseCommand):
    help = "Updates currency exchange rates"
    option_list = BaseCommand.option_list + (
            make_option('-n', '--number',
                action  = 'store',
                type    = 'int',
                dest    = 'num',
                default = 20,
                help    = 'Number of currencies to update'
            ),
            make_option('-a', '--all',
                action  = 'store_true',
                dest    = 'all',
                default = False,
                help    = 'Update all rates (overrides -n)'
            ),
        )
    def handle(self, *args, **options):
        queryset = models.Currency.objects.no_cache().all()
        if not options['all']:
            queryset = queryset.order_by('last_update')[:options['num']]

        for currency in queryset:
            if options['verbosity']>1:
                self.stdout.write(u"updating %s\n"%currency.code)
            models.update_rate(currency)

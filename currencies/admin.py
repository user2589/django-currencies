from django.contrib import admin
from currencies import models


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'code', 'name', 'last_update', 'symbol', 'factor')
    list_editable = ('is_active',)
    list_display_links = ('name', 'code')
    list_filter = ('is_active',)
    actions = ['update_rate']

    def update_rate(self, request, queryset):
        for currency in queryset:
            models.update_rate(currency)

    update_rate.short_description = "Update selected currencies rate"

admin.site.register(models.Currency, CurrencyAdmin)


class CountryCurrencyAdmin(admin.ModelAdmin):
    list_display = ('country', 'currency')
    list_display_links = ('country', 'currency')
admin.site.register(models.CountryCurrency, CountryCurrencyAdmin)

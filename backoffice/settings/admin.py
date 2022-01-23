from django.contrib import admin
from .models import CreditCardInfo, Payment, Store, Receipt, Tax
# Register your models here.


class CreditCardInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'expiration_date')


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('store', 'image_preview', 'header_text', 'footer_text')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'type', 'store')


admin.site.register(CreditCardInfo, CreditCardInfoAdmin)
admin.site.register(Payment)
admin.site.register(Store, StoreAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Tax, TaxAdmin)

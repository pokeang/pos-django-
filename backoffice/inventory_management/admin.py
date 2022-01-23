from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseOrderItem, InventoryCount, DailyReceipt, DailyReceiptDetail
from django.utils.safestring import mark_safe
from django.shortcuts import reverse


# Register your models here.
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address1')


class PurchaseOrderAdmin(admin.ModelAdmin):

    def order_count(self, obj):
        return mark_safe(
            "<a href='{0}?purchase_order__id__exact={1}' class='related-widget-wrapper-link change-related'>{2}</a>".format(
                reverse('admin:inventory_management_purchaseorderitem_changelist'),
                obj.id,
                PurchaseOrderItem.objects.filter(purchase_order=obj).count()
            )
        )
    order_count.short_description = "Item order count"
    list_display = ('purchase_number', 'date_purchase', 'expected_date', 'store_name', 'supplier', 'status', 'order_count')
    list_filter = ('supplier__name', 'status')


class PurchaseOrderItemAdmin(admin.ModelAdmin):

    def link_purchase_order(self, obj):
        return mark_safe("<a href='/admin/inventory_management/purchaseorder/{0}/change' class='related-widget-wrapper-link change-related'>{1}</a>".format(
                obj.purchase_order.id,
                obj.purchase_order
            )
        )

    list_display_links = ('link_purchase_order', 'item')
    list_display = ('link_purchase_order', 'item', 'store_name', 'quantity', 'purchase_cost', 'amount', 'order_status')
    list_filter = ('purchase_order', 'purchase_order__status')


class InventoryCountAdmin(admin.ModelAdmin):
    # Item.objects.filter(item=obj).count()
    def count_item(self, obj):
        return mark_safe(
            "<a href='{0}?store__name={1}' class='related-widget-wrapper-link change-related'>{2}</a>".format(
                reverse('admin:item_storeitem_changelist'),
                obj.store.name.replace(" ", "+"),
                obj.storeItem.all().count()
            )
        )
    def check_stock(self, obj):
        return mark_safe(
            "<a href='{0}?store__name={1}' class='related-widget-wrapper-link change-related'>{2}</a>".format(
                reverse('admin:item_storeitem_changelist'),
                obj.store.name.replace(" ", "+"),
                'check stock'
            )
        )
    list_display_links = ('note', 'count_item', 'check_stock')
    list_display = ('note', 'store', 'count_item', 'check_stock')
    list_filter = ('store__name',)


class DailyReceiptAdmin(admin.ModelAdmin):

    def total_amount(self, obj):
        return mark_safe(
            "<a href='{0}?daily_receipt__id__exact={1}' class='related-widget-wrapper-link change-related'>{2}</a>".format(
                reverse('admin:inventory_management_dailyreceiptdetail_changelist'),
                obj.no_number(),
                DailyReceiptDetail.objects.filter(daily_receipt=obj).count()
            )
        )

    def total_price(self, obj):
        details = DailyReceiptDetail.objects.filter(daily_receipt=obj.id)
        total = 0
        for p in details:
            total += p.total_price()
        return total

    list_display = ('no_number', 'store_name', 'date_sold', 'total_amount', 'total_price')
    list_filter = ('store__name', )


class DailyReceiptDetailAdmin(admin.ModelAdmin):

    def link_daily_receipt(self, obj):
        return mark_safe("<a href='{0}?id={1}' class='related-widget-wrapper-link change-related'>{2}</a>".format(
                reverse('admin:inventory_management_dailyreceipt_changelist'),
                obj.daily_receipt.id,
                obj.daily_receipt
            )
        )
    list_display = ('link_daily_receipt', 'item', 'amount_sold', 'price', 'tax_value', 'discount_value', 'total_price')
    list_filter = ('daily_receipt', )

    list_display_links = ('item', )


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderItem, PurchaseOrderItemAdmin)
admin.site.register(InventoryCount, InventoryCountAdmin)
admin.site.register(DailyReceiptDetail, DailyReceiptDetailAdmin)
admin.site.register(DailyReceipt, DailyReceiptAdmin)

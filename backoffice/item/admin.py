from django.contrib import admin
from .models import Category, Item, StoreItem, Discount

admin.site.site_header = 'POS Administrator'
admin.site.site_title = 'POS Management Admin'
admin.site.index_title = 'Welcome to POS Admin'


# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category_name', 'price', 'cost', 'display')
    list_display_links = ('name', 'image_preview')
    readonly_fields = ('image_preview',)
    search_fields = ('name', 'price', 'cost')
    list_filter = ('display', 'category__name')


class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'item', 'price', 'in_stock', 'low_stock')
    list_filter = ('store__name',)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'type', 'date_start', 'date_end')


admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(StoreItem, StoreItemAdmin)
admin.site.register(Discount, DiscountAdmin)

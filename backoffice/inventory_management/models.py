from django.db import models
from settings.models import Store, Tax
from item.models import Item, StoreItem, Discount


# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(blank=True)
    website = models.CharField(max_length=50, blank=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=45, blank=True)
    postal_code = models.CharField(max_length=45, blank=True)
    country = models.CharField(max_length=45, default='Cambodia')
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'supplier_tbl'


STATUS = [
    (0, ''),
    (1, 'Closed'),
    (2, 'Pending'),
    (3, 'Cancel')
]


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    to_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    date_purchase = models.DateField()
    expected_date = models.DateField()
    status = models.IntegerField(default=0, choices=STATUS, blank=True)
    note = models.TextField(blank=True)

    @property
    def store_name(self):
        return self.to_store.name

    def purchase_number(self):
        return 'PUR%03d'%self.id

    def __str__(self):
        return self.purchase_number()

    class Meta:
        db_table = 'purchase_order_tbl'

# on_delete="SET_NULL"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, default=0)
    purchase_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def amount(self):
        return self.quantity * self.purchase_cost

    def store_name(self):
        return self.purchase_order.store_name

    def order_status(self):
        return STATUS[self.purchase_order.status]

    def __str__(self):
        return self.item.name

    class Meta:
        db_table = 'purchase_order_item_tbl'


class InventoryCount(models.Model):
    note = models.CharField(max_length=500)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, default=0)
    storeItem = models.ManyToManyField(StoreItem)

    def store_id(self):
        return self.store.id

    class Meta:
        db_table = 'inventory_count_tbl'


class DailyReceipt(models.Model):
    store = models.ForeignKey(Store, related_name='store', on_delete=models.CASCADE)
    date_sold = models.DateTimeField(auto_now_add=True)
    # amount = models.IntegerField()
    # total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def no_number(self):
        return 'No%03d'%self.id

    def store_name(self):
        return self.store.name

    def __str__(self):
        return self.no_number()

    class Meta:
        db_table = 'daily_receipt_tbl'


class DailyReceiptDetail(models.Model):
    item = models.ForeignKey(Item, models.CASCADE)
    daily_receipt = models.ForeignKey(DailyReceipt, related_name='daily_receipt_items', on_delete=models.CASCADE)
    amount_sold = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)

    # def no_receipt(self):
    #     return self.daily_receipt
    def item_name(self):
        return self.item.name

    def tax_value(self):
        return self.tax

    def discount_value(self):
        if self.discount:
            if self.discount.type == 2:
                return str(self.discount.value) + '%'
            else:
                return self.discount.value
        else:
            return 0

    def total_price(self):
        total = self.price * self.amount_sold
        # if self.discount > 0:
        #     total + self.discount_value
        # if self.tax_value > 0:
        #     total + self.tax_value
        return total

    def __str__(self):
        return self.item.name

    class Meta:
        db_table = 'daily_receipt_detail_tbl'

import pytz
from django.db import models
from settings.models import Store, Tax
from django.utils.safestring import mark_safe
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def items(self):
        return self.item_set.all()

    class Meta:
        db_table = 'category_tbl'


class Item(models.Model):
    name = models.CharField(max_length=85)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    display = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    cost = models.PositiveIntegerField(null=True, blank=True)
    # sku = models.CharField(max_length=45, null=True, blank=True)
    bar_code = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='item', max_length=254, null=True, blank=True)
    # order = models.IntegerField(null=True, blank=True)
    # store = models.ForeignKey(Store, on_delete=models.CASCADE)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)

    # @property
    # def store_items(self):
    #     return self.storeitem_set.all()

    def category_name(self):
        return self.category.name

    def category_id(self):
        return self.category.id

    def __str__(self):
        return self.name

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" style="width: 65px; height:65px;" style="object-fit:contain" />'.format(self.image.url))
        return '(No image)'
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

    def image_url(self):
        if self.image:
            return self.image.url
        return '/media/no-image.jpg'

    class Meta:
        db_table = 'item_tbl'


class StoreItem(models.Model):
    store = models.ForeignKey(Store, related_name='store_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    in_stock = models.PositiveIntegerField(blank=True, default=0)
    low_stock = models.PositiveIntegerField(blank=True, default=0)
    date_created = models.DateTimeField(default=timezone.now)

    def item_name(self):
        return self.item.name

    def item_id(self):
        return self.item.id

    def store_name(self):
        return self.store.name

    def __str__(self):
        return self.item.name

    class Meta:
        ordering = ('-date_created', )
        db_table = 'store_item_tbl'


class Discount(models.Model):
    TYPES = [
        (1, 'Amount'), (2, 'Percentage')
    ]
    name = models.CharField(max_length=45)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    type = models.PositiveIntegerField(choices=TYPES, default=1)
    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(null=True)

    def type_str(self):
        text = 'Percentage'
        if self.type == 1:
            text = 'Amount'
        return text

    def store_name(self):
        return self.store.name

    def store_id(self):
        return self.store.id

    def item_id(self):
        return self.item.id

    def item_name(self):
        return self.item.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'discount_tbl'

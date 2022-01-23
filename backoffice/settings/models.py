from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
class CreditCardInfo(models.Model):
    name = models.CharField(max_length=45)
    expiration_date = models.DateField(auto_now_add=False, blank=False)
    cvv = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'credit_card_info_tbl'


class Payment(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'payment_tbl'


class Store(models.Model):
    name = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=12)
    address = models.TextField(max_length=150)
    description = models.TextField(max_length=200, blank=True)

    # @property
    # def store_items(self):
    #     return self.storeitem_set.all()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store_tbl'


class Receipt(models.Model):
    LANG = [
        ('en', 'English'),
        ('kh', 'Khmer')
    ]
    printed_receipt_img_logo = models.ImageField(upload_to='receipt')
    header_text = models.CharField(max_length=45)
    footer_text = models.CharField(max_length=45)
    # lang = models.CharField(choices=LANG, default='en', max_length=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def image_preview(self):
        return mark_safe('<img src="{}" style="width: 45px; height:45px;" style="object-fit:contain" />'.format(self.printed_receipt_img_logo.url))

    image_preview.allow_tags = True
    image_preview.short_description = 'Priced Receipt Image Logo'

    def __str__(self):
        return self.store.name

    class Meta:
        db_table = 'receipt_tbl'


class Tax(models.Model):
    TYPES = [
        (1, 'Included in the price'), (2, 'Added to the price')
    ]
    name = models.CharField(max_length=45)
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.IntegerField(choices=TYPES)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def rate_value(self):
        return self.rate

    def __str__(self):
        return self.store.name

    class Meta:
        db_table = 'tax_tbl'

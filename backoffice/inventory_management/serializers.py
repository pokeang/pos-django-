from rest_framework import serializers
from .models import DailyReceipt, DailyReceiptDetail


class DailyReceiptDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReceiptDetail
        fields = ('id', 'item', 'item_name', 'price', 'amount_sold', 'tax', 'tax_value', 'discount',
                  'discount_value', 'total_price')  # '__all__'
        read_only_fields = ('id', 'item_name', 'tax_value', 'date_sold', 'discount_value', 'total_price')


class DailyReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReceipt
        fields = '__all__'


class DailyReceiptsDetailSerializer(serializers.ModelSerializer):
    daily_receipt_items = DailyReceiptDetailSerializer(many=True)

    class Meta:
        model = DailyReceipt
        fields = ('id', 'store', 'store_name', 'no_number', 'date_sold', 'daily_receipt_items')

        read_only_fields = ('id', 'no_number', 'store_name', 'date_sold')
